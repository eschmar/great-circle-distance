#!/bin/bash
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

trials=50
base="geo"
database="geo"

while getopts 't:d:x' flag; do
    case "${flag}" in
        t) trials=$OPTARG ;;
        d) database=$OPTARG ;;
        *) error "Unexpected option ${flag}" ;;
    esac
done

for samples in 100 500 1000 2500 5000 7500 10000 25000 50000 75000 100000 250000 500000 750000 1000000
do
    printf "$samples "
    table="${base}_$(printf %07d $samples)"

    geo="SELECT (6378.137 * acos(cos(radians(ST_X(p1))) * cos(radians(ST_X(p2))) * cos(radians(ST_Y(p2)) - radians(ST_Y(p1))) + sin(radians(ST_X(p1))) * sin(radians(ST_X(p2))))) AS distance FROM ${table} WHERE 1"
    query="SET profiling = 1; $geo; SHOW PROFILES;"

    for (( i=1; i<=$trials; i++ ))
    do
        temp=$(mysql -u root -vvv $database -e "$query" | grep "| SELECT (6378.137" | grep -Eo '[0-9][.][0-9]+[ ]\|' | grep -Eo '[0-9][.][0-9]+')

        printf "$temp"
        if [ $i -lt $trials ]
        then
            printf " "
        fi
    done

    echo
done
