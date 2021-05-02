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
                text-align: center;
                vertical-align: middle;
                color: white;
                font-size: xx-large;
                line-height: 2cm;
                height: 2cm;
                margin-top: 0%;
                margin-bottom: 3%;
                background-color: rgb(192, 116, 182);
            }

            b, p {
                font-family: Arial, Helvetica, sans-serif;
            }

            .center {
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
            }

            .container {
                padding: 30px;
                border-style: solid;
                border-radius: 15px;
                border-color: rgb(116, 175, 116);
                margin: 20px;
            }

            .container-small {
                width: 500px;
                padding: 30px;
                border-style: solid;
                border-radius: 15px;
                border-color: rgb(116, 175, 116);
                margin: auto;
                align-items: center;
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

            button {
                background-color: #04AA6D;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                position: absolute;
                border: none;
                cursor: pointer;
                left: 50%;
                -ms-transform: translate(-50%, -50%);
                transform: translate(-50%, -50%);
            }

            .button1 {width: 100%;}
            .button2 {
                width: 500px;
                margin-top: 1cm;
            }

            button:hover {
                box-shadow: 0 12px 16px 0 rgb(182, 181, 181);
            }

            .radio-input * {
                vertical-align: middle;
                display: inline-block;
            }

            .radio-input label { 
                width:40px;
                display:inline-block;
            }

            input[type=number] {
                height: 0.8cm;
                font-size: 95%;
                border: solid rgb(221, 220, 220) 2px;
                border-radius: 0.25em;
                -moz-appearance: textfield;
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

        </style>
    </head>
    <body>
        {{!base}}
    </body>
</html>
