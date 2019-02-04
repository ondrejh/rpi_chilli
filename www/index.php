<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <meta name="rating" content="general">
    <meta name="author" content="chilli man">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Semínka papriček</title>
    <meta name="description" content="Zobrazení aktuální situace v našem pařníčku. Můžete zde nejen sledovat vývoj teploty a vzdušné vlhkosti, ale také vidíte aktuální foto rostlinek." />
    <meta name="keywords" content="semínka, chilli, moruga, čisté zlo" />

    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/4.0.0/normalize.min.css" media="screen, print" />
    <link rel="stylesheet" type="text/css" href="style.css" media="screen, print" />
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic|Oswald&amp;subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <link rel="shortcut icon" href="favicon.ico" />
</head>

<body class="home">

    <header id="top">
        <h1>Kterak se mají naše semínka (rostlinky)</h1>
    </header>

    <section class="content">

        <article class="main">
            <!--<p class="left">
            <img src="humi.png" alt="Graf teploty a vlhkosti v pařníčku" width="600" height="450" />
            <span class="desc">Graf aktuální teploty a&nbsp;vzdušné vlhkosti</span>
            </p>-->
            <p class="right">
                <img src="chilli.jpg" alt="Jak to v pařníčku aktuálně vypadá" />
                <?php
                    echo '<span class="desc">Aktuální foto - ' . date("H:i",filemtime('chilli.jpg')) . '</span>';
                ?>
            </p>
        </article>

        <article class="archive">
            <h2>Archivní záběry</h2>
            <?php
                function mtimecmp($a, $b) {
                    $mt_a = filemtime($a);
                    $mt_b = filemtime($b);

                    if ($mt_a == $mt_b)
                        return 0;
                    else if ($mt_a < $mt_b)
                        return -1;
                    else
                        return 1;
                }

                $images = glob('archive/*.jpg');
                usort($images, "mtimecmp");
                array_reverse($images);

                for ($i = count($images) - 1; $i >= 0; $i--) {
                    $image = $images[$i];
                    $day = substr($image, 14, 2);
                    $month = substr($image, 12, 2);
                    $year = substr($image, 8, 4);
                    $hour = substr($image, 17, 2);
                    $minute = substr($image, 19, 2);

                    if($hour == '07') {
                        echo '<p class="foto"><img class="fotoImg" src="'.$image.'" />';
                        echo '<span class="name">'.$day.'.'.$month.'.'.$year.' - '.$hour.':'.$minute.'</span></p>';
                    }
                }
            ?>
        </article>
    </section>

    <footer>
        <p>Všechna práva vyhrazena - fotografie mohou být použity jen s&nbsp;písemným souhlasem autora.</p>
        <p>Tento souhlas musí být vyveden ve&nbsp;třech kopiích na&nbsp;pergamenu z&nbsp;oslí kůže, podepsán krví jednorožce, jenž byl uloven v&nbsp;lese Řáholci za&nbsp;bezměsíčné noci.</p>
        <p class="toTop">
            <a href="#top" title="Přejít na horní část stránky">Nahoru</a>
        </p>
    </footer>

    <script type="text/javascript" src="http://code.jquery.com/jquery-2.2.0.min.js" ></script>
    <script type="text/javascript">
        $(document).ready(function (){
            function scrollToTop(aid){
                var aTag = $("[id='"+ aid +"']");
                    $('html,body').animate({scrollTop: aTag.offset().top},'slow');
                }
                $(".toTop a").click(function() {
                scrollToTop('top');
            });
        });
    </script>

</body>
</html>