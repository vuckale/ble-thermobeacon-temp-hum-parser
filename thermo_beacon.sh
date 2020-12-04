#!/usr/bin/bash

get_value() {
    hex_temp1=$1
    hex_temp2=$2
    hex_temp1_trimmed=`echo $hex_temp1`
    hex_temp2_trimmed=`echo $hex_temp2`
    hextemp=$( echo "${hex_temp2_trimmed}${hex_temp1_trimmed}" )
    dectemp=$( echo $((16#$hextemp)) )
    dectemp_double=$( echo ${dectemp})
    b=16
    echo "$(echo "$dectemp $b" | awk '{print $1 / $2}')"

}

while [ ${#out} -lt 1 ] && [ "$chrlen" != 289 ]
do
bluetoothctl_out=$( { printf 'scan on\n\n' ; sleep 10 ; printf 'quit \n\n' ; } | bluetoothctl)
out=$( echo "$bluetoothctl_out" | grep -A 2 "Device $ENV_THERMO_BEACON_MAC ManufacturerData Value:")
chrlen=${#out}
if [ "$chrlen" == 289 ]; then
    # get the string at the position 21 and check if not "..^.......*=..#." 
    checker=$(echo "$out" | cut -d ' ' -f 21)
    checker_trimmed=`echo $checker`
    if [[ "$checker_trimmed" != *"#"* ]] || [[ "$checker_trimmed" != "..^.......*=..#." ]]; then
        hex_temp1=$(echo "$out" | cut -d ' ' -f 14)        
        hex_temp2=$(echo "$out" | cut -d ' ' -f 15)
        hex_hum1=$(echo "$out" | cut -d ' ' -f 16)
        hex_hum2=$(echo "$out" | cut -d ' ' -f 17)
        room_temp=$(echo $(get_value $hex_temp1 $hex_temp2))
        room_hum=$(echo $(get_value $hex_hum1 $hex_hum2))
        echo "$room_temp" | awk '{printf("%0.2f\n",$1)}'  
        echo "$room_hum" | awk '{printf("%0.2f\n",$1)}'
    fi
fi
done
