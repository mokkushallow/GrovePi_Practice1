# GrovePi_Practice1
Practice of GrovePi (Light Sensor, LED bar, RGB LCD Display)

GrovePiの練習用（光量センサ、LEDバー、LCD）

# Setting of GrovePi（GrovePiの準備）
Light sensor -> A0　（光量センサ -> A0）

LED bar -> D5　（LEDバー -> D）

RGB LCD Display -> I2C-2　（RGB LCDディスプレイ -> I2C-2）


# Behavior of this code（プログラム実行内容）
Sensor value is displayed on LCD

光量センサの値がLCDディスプレイに表示される

LED LEVEL is set (0-100:LEVEL1, 101-200:LEVEL2, ... , 801-900:LEVEL9, 900-:LEVEL10) 

100刻みでLED LEVELを設定(0-100:LEVEL1, 101-200:LEVEL2, ... , 801-900:LEVEL9, 900-:LEVEL10) 

LED LEVELに応じてLEDバーが光る（0～10）
