#!/bin/bash

if [ "$1" == "wins" ]; then
    col=2
elif [ "$1" == "losses" ]; then
    col=3
elif [ "$1" == "w/lratio" ]; then
    col=4
fi

games=$(awk -F',' '{print $4}' history.csv |sort|uniq)

for g in $games; do
    if [ "$1" == "namea" ];then
        echo "======= $(echo $g | tr '[:lower:]' '[:upper:]') ======="
        echo "Player | Wins | Losses | W/L Ratio"
        awk -F',' -v game="$g" '
        BEGIN{
            OFS=" | ";
        }
        {
        if($4==game){
            players[$1]=$1;
            players[$2]=$2;
            win[$1]++;
            loss[$2]++;
        }
        }
        END{
            for (p in players){
                if(loss[p]==0){
                wl[p]=win[p];
                } else{
                wl[p]=win[p]/loss[p];
                }
                print p, win[p], loss[p], wl[p];

            }
        }' history.csv | sort -t "|" -d -k 1
    elif [ "$1" == "named" ];then
        echo "======= $(echo $g | tr '[:lower:]' '[:upper:]') ======="
        echo "Player | Wins | Losses | W/L Ratio"
        awk -F',' -v game="$g" '
        BEGIN{
            OFS=" | ";
        }
        {
        if($4==game){
            players[$1]=$1;
            players[$2]=$2;
            win[$1]++;
            loss[$2]++;
        }
        }
        END{
            for (p in players){
                if(loss[p]==0){
                wl[p]=win[p];
                } else{
                wl[p]=win[p]/loss[p];
                }
                print p, win[p], loss[p], wl[p];

            }
        }' history.csv | sort -t "|" -dr -k 1
    else
        echo "======= $(echo $g | tr '[:lower:]' '[:upper:]') ======="
        echo "Player | Wins | Losses | W/L Ratio"
        awk -F',' -v game="$g" '
        BEGIN{
            OFS=" | ";
        }
        {
        if($4==game){
            players[$1]=$1;
            players[$2]=$2;
            win[$1]++;
            loss[$2]++;
        }
        }
        END{
            for (p in players){
                if(loss[p]==0){
                wl[p]=win[p];
                } else{
                wl[p]=win[p]/loss[p];
                }
                print p, win[p], loss[p], wl[p];

            }
        }' history.csv | sort -t "|" -nr -k $col
    fi
done


