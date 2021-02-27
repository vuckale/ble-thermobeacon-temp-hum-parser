#!/usr/bin/python3

import re
import os
import datetime
import time
import subprocess

# thermo beacon max and min values
MAX = 65
MIN = -20

DEVICE_MAC = ""

_log = True
log_file = None

def log_msg(msg):
    global log_file
    log_file.write(msg + "\n")

while True:

    if _log:
        log_file = open("./thermo-beacon-log.txt", "a")

    _log and log_msg("\nstart at ")

    p = subprocess.Popen('{ printf \'scan on\n\n\' ; sleep 10 ; printf \'quit \n\n\' ; } | bluetoothctl', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode("utf-8")
    curr_time = datetime.datetime.now()

    collect = ""
    stripped = []
    for i in out:
        if i == "\n":
            stripped.append(str(collect))
            collect = ""
        else: 
            collect += i

    checkers = ["..^.......*=..#.", "..^.......*=..#.", "..^.......*=....", "..^............."]
    fault = False
    no_data = True

    _log and log_msg(str(curr_time))
    _log and log_msg(str(stripped))

    for i in range(0, len(stripped)):
        if DEVICE_MAC + " ManufacturerData Value:" in stripped[i]:
            no_data = False
            if i+1 < len(stripped):
                bytes_array = stripped[i+1].split(' ')

                _log and log_msg("stripped[i+1]: " + stripped[i+1])
                _log and log_msg("bytes_array = " + str(bytes_array))

                for checker in checkers:
                    if bytes_array[len(bytes_array) - 1] == checker:
                        fault = True
                        break
                if len(bytes_array[len(bytes_array) - 1]) != 16:
                    fault = True
                if not fault:

                    _log and log_msg("checker allright: " + str(bytes_array[len(bytes_array) - 1]))

                    hum_hex = str(bytes_array[len(bytes_array) - 5]) + "" + str(bytes_array[len(bytes_array) - 6])
                    temp_hex = str(bytes_array[len(bytes_array) - 7]) + "" + str(bytes_array[len(bytes_array) - 8])

                    _log and log_msg("hum_hex = " + str(hum_hex))
                    _log and log_msg("temp_hex = " + str(temp_hex))

                    humidity_check = int(float("{:.1f}".format(int(hum_hex, 16) / 16)))
                    temperature_check = int(float("{:.1f}".format(int(temp_hex, 16) / 16)))
                    humidity = "{:.1f}".format(int(hum_hex, 16) / 16)
                    temperature = "{:.1f}".format(int(temp_hex, 16) / 16)

                    _log and log_msg("humidity = " + humidity)
                    _log and log_msg("temperature = " + temperature)

                    if (humidity_check >= 0 or humidity_check <= 100) and (temperature_check >= -20 or temperature_check <= 65):

                        _log and log_msg("humidity = " + str(humidity))
                        _log and log_msg("temperature = " + str(temperature))

                        try:
                            f_name = "./thermo-beacon-out.txt"
                            f = open(f_name, "a")
                            f.write(str(curr_time) + ";" + temperature + "°" + ";" + humidity + "%" + "\n")
                            f.close()
                        except IOError:
                            _log and log_msg("IOError occured, could not write to " + f_name)
                            raise IOError

                        _log and log_msg("Succesfully wrote to " + f_name)

                    else:
                        _log and log_msg("Something is wrong: temperature = " + str(temperature) + " humidity = " + str(humidity))
                else:
                    _log and log_msg("checker failed: " + str(bytes_array[len(bytes_array) - 1]))

    no_data and _log and log_msg("no data")
    _log and log_msg("end\n")
    _log and log_file.close()
