<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Nutrition tracker</title>

        <style>
            h1 {
                font-family: 'Courier New', Courier, monospace;
                color: white;
                line-height: 2cm;
                height: 2cm;
                margin-top: 0%;
                margin-bottom: 3%;
                background-color: rgb(192, 116, 182);
            }

            b, p, a {
                font-family: Arial, Helvetica, sans-serif;
            }

            .naslov {
                float: left;
                text-align: center;
                vertical-align: middle;
                font-size: xx-large;
                padding-left: 43%;
            }
            .naslov-fp {
                padding-left: 43%;
            }

            .center {
                text-align: center;
            }

            .alignleft {
                float: left;
                margin-top: 0.4cm;
                margin-left: 1cm;
                color:white;
                font-family: Arial, Helvetica, sans-serif;
            }

            .alignright {
                float: right;
                margin-top: 0.8cm;
                margin-right: 1cm;
            }

            .container {
                padding: 30px;
                border-style: solid;
                border-radius: 15px;
                border-color:#04AA6D;
                margin: 20px;
            }

            .container-small {
                width: 500px;
                padding: 30px;
                border-style: solid;
                border-radius: 15px;
                border-color: #04AA6D;
                margin: auto;
                align-items: center;
            }

            button {
                background-color: #04AA6D;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                cursor: pointer;
            }

            .button1 {width: 100%; border: none;}
            .button2 {
                width: 500px;
                margin-top: 1cm;
                left: 50%;
                -ms-transform: translate(-50%, -50%);
                transform: translate(-50%, -50%);
                position: absolute;
                border: none;
            }
            .button3 {
                width:4cm; 
                background-color:lightgray;
                display:block;
                margin: 0 auto;
                border: none;
            }
            .button4 {
                height: 0.8cm;
                border-width: 2px;
                border-radius: 6px;
                border-color: white;
                background-color: rgb(192, 116, 182);
                padding-top: 5px;
            }
            .button-izbrisi {
                background-color: transparent;
                border-color: transparent;
                color: #04AA6D;
                font-weight: bold;
                margin: 0 auto;
            }

            button:hover {
                box-shadow: 0 12px 16px 0 rgb(182, 181, 181);
            }

            .button-odjava {
            top: 1em;
            right: 2em;
            float: right
            }

            input[type=text], input[type=password] {
                width: 100%;
                padding: 25px 20px;
                margin: 8px 0;
                height: 10px;
                display: inline-block;
                border: 1px solid #ccc;
                box-sizing: border-box;
                font-size: 95%;
            }

            .radio-input * {
                vertical-align: middle;
                display: inline-block;
            }

            .radio-input label { 
                width:40px;
                display:inline-block;
            }

            input[type=number], input[type=text2] {
                height: 0.8cm;
                font-size: 95%;
                border: solid rgb(221, 220, 220) 2px;
                border-radius: 0.25em;
                -moz-appearance: textfield;
                }

            input[type=date] {
              border-radius: 5px;
              border-color: lightgray;
            }



            #hrana-tabela {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              border-radius: 7px;
              width: 30%;
              margin: 0 auto
            }
            #hrana-tabela td, #hrana-tabela th {
              border: 1px solid #ddd;
              padding: 8px;
            }
            #hrana-tabela th {
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              color: white;
            }

            #vrednosti-tabela {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 60%;
              margin: 0 auto;
              margin-top: 30px;
            }
            #vrednosti-tabela td, #hrana-tabela th {
              border: 1px solid #ddd;
              padding: 8px;
              width: 20%
            }
            #vrednosti-tabela th {
              padding-top: 12px;
              padding-bottom: 12px;
              border-radius: 5px;
              background-color: #04AA6D;
              color: white;
            }

            /* source code: https://codepen.io/vkjgr/pen/VYMeXp */
            select {
                appearance: none;
                position: left;
                font-family: Arial;
                line-height: 0.8cm;
                border-radius: 0.25em;
                border: solid rgb(221, 220, 220) 2px; 
                padding: 0 1em 0 0;
                margin: 0;
                align-items: center;
                width: 100%;

                background-image:
                  linear-gradient(45deg, transparent 50%, gray 50%),
                  linear-gradient(135deg, gray 50%, transparent 50%),
                  linear-gradient(to right, #ccc, #ccc);
                background-position:
                  calc(100% - 20px) calc(1em + 2px),
                  calc(100% - 15px) calc(1em + 2px),
                  calc(100% - 2.5em) 0.5em;
                background-size:
                  5px 5px,
                  5px 5px,
                  1px 1.5em;
                background-repeat: no-repeat;
            }

            select:focus {
                background-image:
                  linear-gradient(45deg, green 50%, transparent 50%),
                  linear-gradient(135deg, transparent 50%, green 50%),
                  linear-gradient(to right, #ccc, #ccc);
                background-position:
                  calc(100% - 15px) 1em,
                  calc(100% - 20px) 1em,
                  calc(100% - 2.5em) 0.5em;
                background-size:
                  5px 5px,
                  5px 5px,
                  1px 1.5em;
                background-repeat: no-repeat;
                border-color: green;
                outline: 0;
            }

            /* Source code: https://css-tricks.com/css3-progress-bars/ */
            .meter { 
              height: 10px;  
              position: static;
              background: rgb(223, 214, 222);
              border-radius: 25px;
              padding: 10px;
              box-shadow: inset 0 -1px 1px rgba(221, 200, 200, 0.3);
              width: 500px;
              margin: 0 auto;
            }
            .meter > span {
              display: block;
              height: 100%;
              border-top-right-radius: 8px;
              border-bottom-right-radius: 8px;
              border-top-left-radius: 20px;
              border-bottom-left-radius: 20px;
              background-color: rgb(136, 77, 128);
              background-image: linear-gradient(
                center bottom,
                rgb(43,194,83) 37%,
                rgb(84,240,84) 69%
              );
              box-shadow: 
                inset 0 2px 9px  rgba(255,255,255,0.3),
                inset 0 -2px 6px rgba(0,0,0,0.4);
              position: relative;
              overflow: hidden;
            }

        </style>
    </head>
    <body>
        {{!base}}
    </body>
</html>
