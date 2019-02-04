#!/usr/bin/python3

import threading
from flask import Flask, request, jsonify
from time import sleep


shared_data = {'light': {'status': 'auto', 'power': 0,
                         'dawn': {'begin': '6:00', 'duration': 30},
                         'dusk': {'begin': '21:00', 'duration': 30}}}
shared_lock = threading.Lock()


class Control(threading.Thread):

    def __init__(self, data=shared_data, lock=shared_lock):
        threading.Thread.__init__(self)

        self.data = data
        self.lock = lock
        self.stop_flag = False

        self.light_status = 'auto'
        self.light_power = 0

    def stop(self):
        self.stop_flag = True

    def run(self):
        while not self.stop_flag:

            if self.light_status != self.data['light']['status']:
                new_status = self.data['light']['status'].lower()
                if new_status != self.data['light']['status']:
                    self.lock.acquire()
                    self.data['light']['status'] = new_status
                    self.lock.release()
                print('Light status has changed from {} to {}'.format(self.light_status, new_status))
                self.light_status = new_status

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

    light = request.args.get('light')
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

    output = 'Light set {}'.format(light)

    return output


if __name__ == '__main__':

    control = Control()
    control.start()

    app.run()

    control.stop()
