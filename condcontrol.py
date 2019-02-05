#!/usr/bin/python3

import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from time import sleep


shared_data = {'light': {'status': 'auto', 'power': 0, 'duration': 'infinite',
                         'dawn': {'begin': '6:00', 'duration': 30},
                         'dusk': {'begin': '20:30', 'duration': 30}},
               'wind': {'status': 'auto', 'power': 0, 'duration': 'infinite',
                        'changes': [['6:30', 50], ['7:30', 0], ['10:00', 70], ['12:15', 0], ['15:30', 40], ['17:00', 0]]}}
shared_lock = threading.Lock()


class Control(threading.Thread):

    def __init__(self, data=shared_data, lock=shared_lock):
        threading.Thread.__init__(self)

        self.data = data
        self.lock = lock
        self.stop_flag = False

        self.light_status = 'auto'
        self.light_power = 0
        self.light_timer = datetime.now()

        self.wind_status = 'auto'
        self.wind_power = 0
        self.wind_timer = datetime.now()

    def stop(self):
        self.stop_flag = True

    def run(self):
        while not self.stop_flag:

            # detect light status change
            if self.light_status != self.data['light']['status']:
                new_status = self.data['light']['status'].lower()
                if new_status != self.data['light']['status']:
                    self.lock.acquire()
                    self.data['light']['status'] = new_status
                    self.data['light']['duration'] = 'infinite' if new_status=='auto' else '15:00'
                    self.lock.release()
                print('Light status has changed from {} to {}'.format(self.light_status, new_status))
                if new_status != 'auto':
                    self.light_timer = datetime.now()
                self.light_status = new_status

            # if light status is AUTO
            if self.light_status == 'auto':
                # calculate light power according to dawn and dusk settings

                today = datetime.today().date()
                now = datetime.now()
                dawn_begin = datetime.combine(today,
                                              datetime.strptime(self.data['light']['dawn']['begin'], "%H:%M").time())
                dawn_end = dawn_begin + timedelta(minutes=self.data['light']['dusk']['duration'])
                dusk_begin = datetime.combine(today,
                                              datetime.strptime(self.data['light']['dusk']['begin'], "%H:%M").time())
                dusk_end = dusk_begin + timedelta(minutes=self.data['light']['dusk']['duration'])

                if now <= dawn_begin:
                    light_set = 0
                elif now < dawn_end:
                    duration = (dawn_end - dawn_begin).total_seconds()
                    status = (now - dawn_begin).total_seconds()
                    light_set = int(round((status / duration) * 100, 0))
                elif now <= dusk_begin:
                    light_set = 100
                elif now < dusk_end:
                    duration = (dusk_end - dusk_begin).total_seconds()
                    status = (dusk_end - now).total_seconds()
                    light_set = int(round((status / duration) * 100, 0))
                else:
                    light_set = 0

            # if light status ON or OFF
            else:
                # set power according to /light/power
                light_set = self.data['light']['power']
                # check on/off status timeout
                duration = datetime.now() - self.light_timer
                if duration > timedelta(minutes=15):
                    self.light_status = 'auto'
                    self.lock.acquire()
                    self.data['light']['status'] = self.light_status
                    self.data['light']['duration'] = 'infinite'
                    self.lock.release()
                else:
                    stot = 15*60 - duration.total_seconds()
                    s = int(round(stot % 60, 0))
                    m = int(round(stot // 60, 0))
                    self.lock.acquire()
                    self.data['light']['duration'] = "{:02d}:{:02d}".format(m, s)
                    self.lock.release()

            # change light power if requested
            if self.light_power != light_set:
                if self.light_power < light_set:
                    self.light_power += 1
                elif self.light_power > light_set:
                    self.light_power -= 1
                print('Change LIGHT power: {}%'.format(self.light_power))

            if self.data['light']['power'] != light_set:
                self.lock.acquire()
                self.data['light']['power'] = light_set
                self.lock.release()

            # detect wind status change
            if self.wind_status != self.data['wind']['status']:
                new_status = self.data['wind']['status'].lower()
                if new_status != self.data['wind']['status']:
                    self.lock.acquire()
                    self.data['wind']['status'] = new_status
                    self.data['wind']['duration'] = 'infinite' if new_status == 'auto' else '15:00'
                    self.lock.release()
                print('Wind status has changed from {} to {}'.format(self.wind_status, new_status))
                if new_status != 'auto':
                    self.wind_timer = datetime.now()
                self.wind_status = new_status

            # if wind status is AUTO
            if self.wind_status == 'auto':
                wind_set = self.data['wind']['changes'][-1][1]
                today = datetime.today().date()
                now = datetime.now()
                for i in range(len(self.data['wind']['changes'])):
                    c = self.data['wind']['changes'][i][0]
                    dtc = datetime.combine(today, datetime.strptime(c, "%H:%M").time())
                    if now < dtc:
                        ii = i-1
                        if ii >= 0:
                            wind_set = self.data['wind']['changes'][ii][1]
                            break

            # if wind status is ON or OFF
            else:
                # set power according to /wind/power
                wind_set = self.data['wind']['power']
                # check on/off status timeout
                duration = datetime.now() - self.wind_timer
                if duration > timedelta(minutes=15):
                    self.wind_status = 'auto'
                    self.lock.acquire()
                    self.data['wind']['status'] = self.wind_status
                    self.data['wind']['duration'] = 'infinite'
                    self.lock.release()
                else:
                    stot = 15*60 - duration.total_seconds()
                    s = int(round(stot % 60, 0))
                    m = int(round(stot // 60, 0))
                    self.lock.acquire()
                    self.data['wind']['duration'] = "{:02d}:{:02d}".format(m, s)
                    self.lock.release()

            # change wind power if requested
            if self.wind_power != wind_set:
                if self.wind_power < wind_set:
                    self.wind_power += 1
                elif self.wind_power > wind_set:
                    self.wind_power -= 1
                print('Change WIND power: {}%'.format(self.wind_power))

            if self.data['wind']['power'] != wind_set:
                self.lock.acquire()
                self.data['wind']['power'] = wind_set
                self.lock.release()

            sleep(0.1)


app = Flask(__name__)


@app.route('/')
def output_json():

    shared_lock.acquire()
    output = jsonify(shared_data)
    shared_lock.release()

    return output


@app.route('/set', methods=['GET', 'POST'])
def set_input():

    output = ''

    light = request.args.get('light')
    wind = request.args.get('wind')

    if light is not None:
        power = None
        try:
            power = int(light)
        except:
            pass

        if power is not None:
            if 1 <= power <= 100:
                shared_lock.acquire()
                shared_data['light']['status'] = 'ON'
                shared_data['light']['power'] = power
                shared_lock.release()
                light = 'ON {}%'.format(power)
            elif power == 0:
                shared_lock.acquire()
                shared_data['light']['status'] = 'OFF'
                shared_data['light']['power'] = power
                shared_lock.release()
                light = 'OFF'
            else:
                light = 'ERROR power input not in 0-100% ({} set)'.format(power)
        else:
            try:
                light = light.lower()
            except:
                light = None

            if light is not None:
                if light == 'on':
                    shared_lock.acquire()
                    shared_data['light']['status'] = 'ON'
                    shared_data['light']['power'] = 100
                    shared_lock.release()
                    light = 'ON 100%'
                elif light == 'off':
                    shared_lock.acquire()
                    shared_data['light']['status'] = 'OFF'
                    shared_data['light']['power'] = 0
                    shared_lock.release()
                    light = 'OFF'
                elif light == 'auto':
                    shared_lock.acquire()
                    shared_data['light']['status'] = 'AUTO'
                    shared_lock.release()
                    light = 'AUTO'

        if light is None:
            light = 'ERROR'

        output += 'Light set {}\n'.format(light)

    if wind is not None:
        power = None
        try:
            power = int(wind)
        except:
            pass

        if power is not None:
            if 1 <= power <= 100:
                shared_lock.acquire()
                shared_data['wind']['status'] = 'ON'
                shared_data['wind']['power'] = power
                shared_lock.release()
                wind = 'ON {}%'.format(power)
            elif power == 0:
                shared_lock.acquire()
                shared_data['wind']['status'] = 'OFF'
                shared_data['wind']['power'] = power
                shared_lock.release()
                wind = 'OFF'
            else:
                wind = 'ERROR power input not in 0-100% ({} set)'.format(power)
        else:
            try:
                wind = wind.lower()
            except:
                wind = None

            if wind is not None:
                if wind == 'on':
                    shared_lock.acquire()
                    shared_data['wind']['status'] = 'ON'
                    shared_data['wind']['power'] = 100
                    shared_lock.release()
                    wind = 'ON 100%'
                elif wind == 'off':
                    shared_lock.acquire()
                    shared_data['wind']['status'] = 'OFF'
                    shared_data['wind']['power'] = 0
                    shared_lock.release()
                    wind = 'OFF'
                elif wind == 'auto':
                    shared_lock.acquire()
                    shared_data['wind']['status'] = 'AUTO'
                    shared_lock.release()
                    wind = 'AUTO'

        if wind is None:
            wind = 'ERROR'

        output += 'Wind set {}\n'.format(wind)

    if output == '':
        output = 'Request error!'

    return output


if __name__ == '__main__':

    print(datetime.now())

    control = Control()
    control.start()

    app.run()

    control.stop()
