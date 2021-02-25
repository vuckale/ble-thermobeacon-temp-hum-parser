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
debug = True
while True:
    if debug:
        debug_file = open("./debug.txt", "a")
    debug and debug_file.write("\nstart at ")
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
    # debug and debug_file.write(str(stripped))
    checkers = ["..^.......*=..#.", "..^.......*=..#.", "..^.......*=....", "..^............."]
    fault = False
    no_data = True
    debug and debug_file.write(str(curr_time) + "\n")
    for i in range(0, len(stripped)):
        if DEVICE_MAC + " ManufacturerData Value:" in stripped[i]:
            no_data = False
            # print(stripped[i])
            if i+1 < len(stripped):
                debug and debug_file.write("stripped[i+1]: " + stripped[i+1])
                bytes_array = stripped[i+1].split(' ')
                debug and debug_file.write("bytes_array = " + str(bytes_array) + "\n")
                debug and debug_file.write("len(bytes_array) = " + str(len(bytes_array)))
                for checker in checkers:
                    if bytes_array[len(bytes_array) - 1] == checker:
                        fault = True
                        break
                if not fault and len(bytes_array) == 21:
                    debug and debug_file.write("checker allright: " + str(bytes_array[len(bytes_array) - 1]) + "\n")
                    hum_hex = str(bytes_array[len(bytes_array) - 5]) + "" + str(bytes_array[len(bytes_array) - 6])
                    temp_hex = str(bytes_array[len(bytes_array) - 7]) + "" + str(bytes_array[len(bytes_array) - 8])
                    debug and debug_file.write("hum_hex = " + str(hum_hex) + "\n")
                    debug and debug_file.write("temp_hex = " + str(temp_hex) + "\n")
                    humidity_check = int(float("{:.1f}".format(int(hum_hex, 16) / 16)))
                    temperature_check = int(float("{:.1f}".format(int(temp_hex, 16) / 16)))
                    humidity = "{:.1f}".format(int(hum_hex, 16) / 16)
                    temperature = "{:.1f}".format(int(temp_hex, 16) / 16)
                    debug and debug_file.write("humidity = " + humidity + "\n")
                    debug and debug_file.write("temperature = " + temperature + "\n")
                    print(temperature)
                    print(humidity)
                    if (humidity_check >= 0 or humidity_check <= 100) and (temperature_check >= -20 or temperature_check <= 65):
                        debug and debug_file.write("humidity = " + str(humidity) + "\n")
                        debug and debug_file.write("temperature = " + str(temperature) + "\n")
                        try:
                            f_name = "./out.txt"
                            f = open(f_name, "a")
                            f.write(str(curr_time) + ";" + temperature + "°" + ";" + humidity + "%" + "\n")
                            f.close()
                        except IOError:
                            debug and debug_file.write("IOError occured, could not write to " + f_name + "\n")
                            raise IOError
                        debug and debug_file.write("Succesfully wrote to " + f_name + "\n")
                    else:
                        debug and debug_file.write("Something is wrong: temperature = " + str(temperature) + " humidity = " + str(humidity) + "\n")
                else:
                    debug and debug_file.write("checker failed: " + str(bytes_array[len(bytes_array) - 1]) + "\n")
    no_data and debug and debug_file.write("no data\n")
    debug and debug_file.write("end\n")
    debug and debug_file.close()
