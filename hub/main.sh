#!/bin/bash
echo "THE MINI GAME HUB v1.0"
echo "=============================="
echo -e " What do you want to do?\n1.Play Games with Friends\n2.Manage account\n(Enter the number corresponding to the option):"
read option
if [[ "$option" == "1" ]]; then
    echo "Hello there players! Enter your usernames and passwords to start playing."
    while true; do
        echo -e "\e[33mPlayer 1 username:"
        read usn1
        echo -e "\e[33mPlayer 1 password:"
        read -s pass1
        pass1_hash=$(echo -n "$pass1" | sha256sum | awk '{print $1}')
        if [[ $(grep -c "User:$usn1" users.tsv) -eq 0 ]]; then
            echo -e "\e[33mYou seem new here!!! Do you want to register (Y/N):"
            read ans
            if [[ "$ans" == "Y" ]]; then
                if [[ ${#pass1} -lt 7 ]]; then
                    echo -e "\e[31mPassword Too Short, should be more than or equal to 7 Characters"
                    continue
                else
                    echo "User:$usn1,Pass:$pass1_hash" >> users.tsv
                    echo -e "\e[32mWelcome $usn1"
                    break
                fi
            else
                continue
            fi
        elif [[ $(grep -c "User:$usn1,Pass:$pass1_hash" users.tsv) -eq 0 ]]; then
            echo -e "\e[31mPlease enter correct password"
            continue
        else
            echo -e "\e[32mWelcome $usn1"
            break
        fi
    done
    while true; do
        echo -e "\e[33mPlayer 2 username:"
        read usn2
        if [[ "$usn2" == "$usn1" ]]; then
            echo -e "\e[31mYou cannot play against yourself, please enter a different username"
            continue
        fi
        echo -e "\e[33mPlayer 2 password:"
        read -s pass2
        pass2_hash=$(echo -n "$pass2" | sha256sum | awk '{print $1}')
        if [[ $(grep -c "User:$usn2" users.tsv) -eq 0 ]]; then
            echo -e "\e[33mYou seem new here!!! Do you want to register (Y/N):"
            read ans
            if [[ "$ans" == "Y" ]]; then
            if [[ ${#pass2} -lt 7 ]]; then
                    echo -e "\e[31mPassword Too Short, should be more than or equal to 7 Characters"
                    continue
                else
                    echo "User:$usn2,Pass:$pass2_hash" >> users.tsv
                    echo -e "\e[32mWelcome $usn2"
                    break
                fi
            else
                continue
            fi
        elif [[ $(grep -c "User:$usn2,Pass:$pass2_hash" users.tsv) -eq 0 ]]; then
            echo -e "\e[31mPlease enter correct password"
            continue
        else
            echo -e "\e[32mWelcome $usn2"
            break
        fi
    done
    python3 game.py "$usn1" "$usn2"
elif [[ "$option" == "2" ]]; then
    while true; do
        echo -e "\e[33mPlayer username:"
        read usn
        if [[ $(grep -c "User:$usn" users.tsv) -eq 0 ]]; then
            echo -e "\e[31mPlayer not found, please enter correct username"
            continue
        else
            break
        fi
    done
    while true; do
        echo -e "\e[33mPlayer password:"
        read -s pass
        pass_hash=$(echo -n "$pass" | sha256sum | awk '{print $1}')
        if [[ $(grep -c "User:$usn,Pass:$pass_hash" users.tsv) -eq 0 ]]; then
            echo -e "\e[31mPlease enter correct password"
            continue
        else
            break
        fi
    done
    echo -e "\e[32mWelcome $usn"
    echo -e "\e[33mWhat do you want to do?\n1.Change Password\n2.Delete Account\n(Enter the number corresponding to the option):"
    read acc_option
    if [[ "$acc_option" == "1" ]]; then
        while true; do
            echo -e "\e[33mEnter new password:"
            read -s new_pass
            if [[ ${#new_pass} -lt 7 ]]; then
                echo -e "\e[31mPassword Too Short, should be more than or equal to 7 Characters"
                continue
            elif [[ "$new_pass" == "$pass" ]]; then
                echo -e "\e[31mNew password cannot be same as old password, please enter a different password"
                continue
            else
                new_pass_hash=$(echo -n "$new_pass" | sha256sum | awk '{print $1}')
                sed -i "s/User:$usn,Pass:$pass_hash/User:$usn,Pass:$new_pass_hash/g" users.tsv
                echo -e "\e[32mPassword changed successfully"
                break
            fi
        done
    elif [[ "$acc_option" == "2" ]]; then
        sed -i "/User:$usn,Pass:$pass_hash/d" users.tsv
        echo -e "\e[32mAccount deleted successfully"
    else
        echo -e "\e[31mInvalid option, please enter a valid option"
    fi
else
    echo -e "\e[31mInvalid option, please enter a valid option"
fi