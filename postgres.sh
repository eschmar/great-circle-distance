#!/bin/bash
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

base='geo'
trials=50
units='false'
color='false'

while getopts 't:uc' flag; do
    case "${flag}" in
        t) trials=$OPTARG ;;
        u) units='true' ;;
        *) error "Unexpected option ${flag}" ;;
    esac
done

for samples in 100 500 1000 2500 5000 7500 10000 25000 50000 75000 100000 250000 500000 750000 1000000
do
    printf "$samples "
    table="${base}_$(printf %07d $samples)"

    # Mile to km conversion. 25146/15625=1.609344.
    query="SELECT (p1 <@> p2) * 1.609344 AS distance FROM $table WHERE True;"

    for (( i=1; i<=$trials; i++ ))
    do
        case $units in
            'true')
                temp=$(echo "\\timing on \\\\ $query" | psql | grep "Time:" | sed s/"Time: "//)
                ;;
            'false')
                temp=$(echo "\\timing on \\\\ $query" | psql | grep "Time:" | grep -Eo -m 1 '[0-9]+([.][0-9]+)?' | head -1)
                ;;
        esac

        printf "$temp"
        if [ $i -lt $trials ]
        then
            printf " "
        fi
    done

    echo
done
