<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <meta name="rating" content="general">
    <meta name="author" content="chilli man">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Semínka papriček - graf</title>
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
            <div id='chart'></div>

            <?php
                $db = new SQLite3("/var/www/html/sensor.sql");
                $query = "SELECT * FROM data ORDER BY timestamp";
                $db_data = $db->query($query);
                $entries = array();
                while($row = $db_data->fetchArray()) {
                    $entries[] = array($row['timestamp'], $row['humidity'], $row['temperature']);
                    #echo sprintf("%s %.1f%% %.1f°C<br>\n", $row['timestamp'], $row['humidity'], $row['temperature']);
                }
                #foreach ($entries as $e) {
                #    echo $e[0]. " ". $e[1]. " ". $e[2]. "<br>\n";
                #}
            ?>

            <script>
                var t1col = '#B21B04';
                var t2col = '#2E4AA9';
                var trace1 = {
                    x: [<?php
                        $first = true;
                        foreach ($entries as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            #echo "'". date('Y-m-d H:i:s', strtotime($e[0])). "'";
                            echo "'". $e[0]. "'";
                        }
                        ?>],
                    y: [<?php
                        $first = true;
                        foreach ($entries as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            echo round($e[1],1);
                        }
                        ?>],
                    name: 'teplota [°C]',
                    type: 'scatter',
                    line: {
                        color: t1col
                    }
                };
                var trace2 = {
                    x: [<?php
                        $first = true;
                        foreach ($entries as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            #echo "'". date('Y-m-d H:i:s', strtotime($e[0])). "'";
                            echo "'". $e[0]. "'";
                        }
                        ?>],
                    y: [<?php
                        $first = true;
                        foreach ($entries as $e) {
                            if ($first) $first = false;
                            else echo ', ';
                            echo round($e[2],1);
                        }
                        ?>],
                    name: 'vlhkost [%]',
                    yaxis: 'y2',
                    type: 'scatter',
                    line: {
                        color: t2col
                    }
                };
                var data = [trace1, trace2];
                var layout = {
                    yaxis: {
                        title: 'teplota [°C]',
                        titlefont: {color: t1col},
                        tickfont: {color: t1col}
                    },
                    yaxis2: {
                        title: 'vlhkost [%]',
                        titlefont: {color: t2col},
                        tickfont: {color: t2col},
                        overlaying: 'y',
                        side: 'right'
                    },
                    margin: { t: 0},
                    showlegend: false
                };
                Plotly.newPlot('chart', data, layout);
            </script>
        </article>

    </section>
</body>
</html>
