EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Sensor:DHT11 U2
U 1 1 6192423A
P 4950 4500
F 0 "U2" H 4706 4546 50  0000 R CNN
F 1 "DHT11" H 4706 4455 50  0000 R CNN
F 2 "Sensor:Aosong_DHT11_5.5x12.0_P2.54mm" H 4950 4100 50  0001 C CNN
F 3 "http://akizukidenshi.com/download/ds/aosong/DHT11.pdf" H 5100 4750 50  0001 C CNN
	1    4950 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 4700 4050 4450
$Comp
L Transistor_BJT:2N2219 Q1
U 1 1 618DBD9E
P 3950 4900
F 0 "Q1" H 4140 4946 50  0000 L CNN
F 1 "2N2219" H 4140 4855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-39-3" H 4150 4825 50  0001 L CIN
F 3 "http://www.onsemi.com/pub_link/Collateral/2N2219-D.PDF" H 3950 4900 50  0001 L CNN
	1    3950 4900
	1    0    0    -1  
$EndComp
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 61927386
P 6400 3400
F 0 "J1" H 6400 4881 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 6400 4790 50  0000 C CNN
F 2 "" H 6400 3400 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 6400 3400 50  0001 C CNN
	1    6400 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 2100 6200 1900
$Comp
L Analog_ADC:MCP3008 U1
U 1 1 61945BF4
P 8200 2900
F 0 "U1" H 8200 3581 50  0000 C CNN
F 1 "MCP3008" H 8200 3490 50  0000 C CNN
F 2 "" H 8300 3000 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf" H 8300 3000 50  0001 C CNN
	1    8200 2900
	0    1    1    0   
$EndComp
$Comp
L Motor:Motor_DC M1
U 1 1 618DC8AF
P 4050 4150
F 0 "M1" H 4208 4146 50  0000 L CNN
F 1 "Water Pump" H 4208 4055 50  0000 L CNN
F 2 "" H 4050 4060 50  0001 C CNN
F 3 "~" H 4050 4060 50  0001 C CNN
	1    4050 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 4500 5400 4500
Wire Wire Line
	5400 4500 5400 4000
Wire Wire Line
	5400 4000 5600 4000
Wire Wire Line
	6200 1900 4950 1900
Wire Wire Line
	4950 4200 4950 1900
Wire Wire Line
	3700 4900 3750 4900
Wire Wire Line
	6700 4700 6700 5300
Wire Wire Line
	4050 5100 4050 5300
Wire Wire Line
	4050 5300 4950 5300
Wire Wire Line
	4950 4800 4950 5300
Connection ~ 4950 5300
Wire Wire Line
	4950 5300 6700 5300
Connection ~ 4950 1900
Wire Wire Line
	4950 1900 4050 1900
Wire Wire Line
	4050 1900 4050 3950
Wire Wire Line
	7200 3900 8300 3900
Wire Wire Line
	8300 3900 8300 3500
Wire Wire Line
	6700 5300 7600 5300
Wire Wire Line
	7600 5300 7600 3100
Connection ~ 6700 5300
Connection ~ 7600 3100
Wire Wire Line
	7600 3100 7600 2800
Wire Wire Line
	8200 3500 8200 3700
Wire Wire Line
	8200 3700 7200 3700
Wire Wire Line
	8100 3500 8100 3800
Wire Wire Line
	8100 3800 7200 3800
Wire Wire Line
	8000 3500 8000 3600
Wire Wire Line
	8000 3600 7200 3600
Wire Wire Line
	5600 3400 3700 3400
Wire Wire Line
	3700 3400 3700 4900
$Comp
L DFRobot:SKU_SEN0114 S1
U 1 1 619C8B6D
P 8800 4750
F 0 "S1" H 8983 5115 50  0000 C CNN
F 1 "SKU_SEN0114" H 8983 5024 50  0000 C CNN
F 2 "" H 9100 4750 50  0001 C CNN
F 3 "" H 9100 4750 50  0001 C CNN
	1    8800 4750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8700 1900 6600 1900
Wire Wire Line
	6600 1900 6600 2100
Wire Wire Line
	8700 1900 8700 2800
Connection ~ 8700 2800
Wire Wire Line
	8700 2800 8700 3100
Connection ~ 8700 3100
Wire Wire Line
	8700 3100 8700 4300
Wire Wire Line
	8950 4300 8950 2150
Wire Wire Line
	8950 2150 8500 2150
Wire Wire Line
	8500 2150 8500 2300
Wire Wire Line
	9100 4750 9100 5300
Wire Wire Line
	9100 5300 7600 5300
Connection ~ 7600 5300
$EndSCHEMATC
