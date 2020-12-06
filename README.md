# bluetoothctl-thermobeacon-temp-hum-parser
### Description:
A simple bash script that captures BLE packages, parses temperature and humidity values and prints them to `stdout`
### Required packages:
```
sudo apt install bluez mawk grep
```
### Usage:
```
script name: thermo_beacon.sh
usage: ./thermo_beacon.sh [options]
options: -h              this help
         --temperature   get temperature value in C°
         --humidity      get humidity value in %
         --csv           output csv formatted line (both --temperature and --humidity are automatically set - if you set them individually they'll be ignored)
```