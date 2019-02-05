<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <meta name="rating" content="general">
    <meta name="author" content="chilli man">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Semínka papriček - servis</title>
    <meta name="description" content="Zobrazení aktuální situace v našem pařníčku. Můžete zde nejen sledovat vývoj teploty a vzdušné vlhkosti, ale také vidíte aktuální foto rostlinek." />
    <meta name="keywords" content="semínka, chilli, moruga, čisté zlo" />

    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/4.0.0/normalize.min.css" media="screen, print" />
    <link rel="stylesheet" type="text/css" href="style.css" media="screen, print" />
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic|Oswald&amp;subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <link rel="shortcut icon" href="favicon.ico" />
    <script src="plotly-latest.min.js"></script>
</head>

<body class="home">

    <header id="top">
        <h1>Kterak se mají naše semínka (rostlinky)</h1>
    </header>

    <section class="content">

        <article class="main">
            <?php
                $data = get_object_vars(json_decode(file_get_contents("http://127.0.0.1:5000")));
                $dlight = get_object_vars($data['light']);
                $dwind = get_object_vars($data['wind']);
                $ddusk = get_object_vars($dlight['dusk']);
                $ddawn = get_object_vars($dlight['dawn']);
                
                echo "<p>Světlo: ". strtoupper($dlight['status']). " ". $dlight['power']. "%</p>". PHP_EOL;
                echo "<p>Větrání: ". strtoupper($dwind['status']). " ". $dwind['power']. "%</p>". PHP_EOL;

                function time2hrs($timestring) {
                    $spl = explode(':', $timestring);
                    $hrs = $spl[0] + $spl[1] / 60;
                    return $hrs;
                }
            
                $time = strtotime($ddawn['begin']);
                $dawnbegin = time2hrs(date("H:i", $time));
                $dawnend = time2hrs(date("H:i", strtotime("+{$ddawn['duration']} minutes", $time)));
                $time = strtotime($ddusk['begin']);
                $duskbegin = time2hrs(date("H:i", $time));
                $duskend = time2hrs(date("H:i", strtotime("+{$ddusk['duration']} minutes", $time)));
            ?>
            
            <div id='chart'></div>
            <script>
                var t1col = '#B21B04';
                var t2col = '#2E4AA9';
                var trace1 = {
                    x: [<?php
                        echo "0, ". $dawnbegin. ", ". $dawnend. ", ". $duskbegin. ", ". $duskend. ", 24";
                        ?>],
                    y: [0, 0, 100, 100, 0, 0],
                    name: 'přísvit [%]',
                    type: 'scatter',
                    line: {
                        color: t1col
                    }
                };
                var trace2 = {
                    x: [<?php
                        echo "0, ";
                        $last = 0;
                        foreach ($dwind['changes'] as $c) {
                            echo time2hrs($c[0]). ", ". time2hrs($c[0]). ", ";
                            $last = $c[1];
                        }
                        echo "24";
                        ?>],
                    y: [<?php
                        echo $last. ", ";
                        foreach ($dwind['changes'] as $c) {
                            echo $last. ", ". $c[1]. ", ";
                            $last = $c[1];
                        }
                        echo $last;
                        ?>],
                    name: 'větrání [%]',
                    type: 'scatter',
                    line: {
                        color: t2col
                    }
                };
                var data = [trace1, trace2];
                var layout = {
                    xaxis: {
                        title: 'čas [h]',
                        range: [0, 24],
                        autotick: false
                    },
                    yaxis: {
                        title: 'výkon [%]'
                    },
                    margin: { t: 0},
                    showlegend: false
                };
                Plotly.newPlot('chart', data, layout);

            </script>
            
            <?php
                // get user info
                $ip=$_SERVER['REMOTE_ADDR'];
                $host_name = gethostbyaddr($_SERVER['REMOTE_ADDR']);

                // set light
                if (isset($_GET["light"])) {
                    $light = strtoupper($_GET["light"]);
                    if (($light === 'ON') or ($light === 'OFF') or ($light === 'AUTO')) {
                        file_get_contents("http://127.0.0.1:5000/set?light=". $light);
                        echo '<p>Host '. $host_name. ' ('. $ip. ') set light '. $light. "</p>". PHP_EOL;
                    }
                    else {
                        $power = intval($light);
                        if (($power > 1) and ($power < 100)) {
                            file_get_contents("http://127.0.0.1:5000/set?light={$power}");
                            echo "<p>Host ". $host_name. " (". $ip. ") set light {$power}%</p>". PHP_EOL;
                        }
                    }
                }
                
                // set wind
                if (isset($_GET["wind"])) {
                    $wind = strtoupper($_GET["wind"]);
                    if (($wind === 'ON') or ($wind === 'OFF') or ($wind === 'AUTO')) {
                        file_get_contents("http://127.0.0.1:5000/set?wind=". $wind);
                        echo '<p>Host '. $host_name. ' ('. $ip. ') set wind '. $wind. "</p>". PHP_EOL;
                    }
                    else {
                        $power = intval($wind);
                        if (($power > 1) and ($power < 100)) {
                            file_get_contents("http://127.0.0.1:5000/set?wind={$power}");
                            echo "<p>Host ". $host_name. " (". $ip. ") set wind {$power}%</p>". PHP_EOL;
                        }
                    }
                }
            ?>
        </article>

    </section>
</body>
</html>