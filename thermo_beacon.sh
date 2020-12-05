#!/usr/bin/bash

function get_value() {
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

function usage()
{
    me=`basename "$0"`
    echo "script name: $me"
    echo "usage: "./$me" [options]"
    echo "options: -h              this help
         --temperature   get temperature value in C°
         --humidity      get humidity value in %"
}

temp_flag=0
hum_flag=0
while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    # VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --temperature)
            temp_flag=1
            ;;
        --humidity)
            hum_flag=1
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done

checker_trimmed="..^.......*=..#."
while [ ${#out} -lt 1 ] || [ "$chrlen" != 289 ] || [ "$checker_trimmed" == "..^.......*=..#." ] || [ "$checker_trimmed" == "..^.......*=...." ]
do
bluetoothctl_out=$( { printf 'scan on\n\n' ; sleep 10 ; printf 'quit \n\n' ; } | bluetoothctl)
out=$( echo "$bluetoothctl_out" | grep -A 2 "Device $ENV_THERMO_BEACON_MAC ManufacturerData Value:")
chrlen=${#out}
# get the string at the position 21 and check if not "..^.......*=..#."
checker=$(echo "$out" | cut -d ' ' -f 21)
checker_trimmed=`echo $checker`
hex_temp1=$(echo "$out" | cut -d ' ' -f 14)
hex_temp2=$(echo "$out" | cut -d ' ' -f 15)
hex_hum1=$(echo "$out" | cut -d ' ' -f 16)
hex_hum2=$(echo "$out" | cut -d ' ' -f 17)
done

if [ "$temp_flag" == 1 ]; then
    room_temp=$(echo $(get_value $hex_temp1 $hex_temp2))
    echo "$room_temp" | awk '{printf("%0.2f\n",$1)}'
fi

if [ "$hum_flag" == 1 ]; then
    room_hum=$(echo $(get_value $hex_hum1 $hex_hum2))
    echo "$room_hum" | awk '{printf("%0.2f\n",$1)}'
fi
