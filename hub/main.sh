#!/bin/bash

echo "Hello there players! Enter your usernames and passwords to start playing."
while true; do
    echo "Player 1 username:"
    read usn1
    echo "Player 1 password:"
    read -s pass1
    pass1_hash=$(echo -n "$pass1" | sha256sum)
    if [[ $(grep -c "User:$usn1" users.tsv) -eq 0 ]]; then
        echo "You seem new here!!! Do you want to register (Y/N):"
        read ans
        if [[ "$ans" == "Y" ]]; then
            if [[ ${#pass1} -lt 7 ]]; then
                echo "Password Too Short, should be more than or equal to 7 Characters"
                continue
            else
                echo "User:$usn1,Pass:$pass1_hash" >> users.tsv
                echo "Welcome $usn1"
                break
            fi
        else
            continue
        fi
    elif [[ $(grep -c "User:$usn1,Pass:$pass1_hash" users.tsv) -eq 0 ]]; then
        echo "Please enter correct password"
        continue
    else
        echo "Welcome $usn1"
        break
    fi
done
while true; do
    echo "Player 2 username:"
    read usn2
    echo "Player 2 password:"
    read -s pass2
    pass2_hash=$(echo -n "$pass2" | sha256sum)
    if [[ $(grep -c "User:$usn2" users.tsv) -eq 0 ]]; then
        echo "You seem new here!!! Do you want to register (Y/N):"
        read ans
        if [[ "$ans" == "Y" ]]; then
           if [[ ${#pass2} -lt 7 ]]; then
                echo "Password Too Short, should be more than or equal to 7 Characters"
                continue
            else
                echo "User:$usn2,Pass:$pass2_hash" >> users.tsv
                echo "Welcome $usn2"
                break
            fi
        else
            continue
        fi
    elif [[ $(grep -c "User:$usn2,Pass:$pass2_hash" users.tsv) -eq 0 ]]; then
        echo "Please enter correct password"
        continue
    else
        echo "Welcome $usn2"
        break
    fi
done
python game.py $usn1 $usn2

