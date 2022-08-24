#!/bin/bash

##################################
## Encrypt Files using Openssl  ##
##################################

install_ssl() {
	[ ! $(command -v openssl) ] && {
		if [ $(command -v pkg) ]; then
			pkg install openssl-tool -y
		elif [ $(command -v apt) ]; then
			sudo apt install openssl -y
		else
			echo "[!] Unfamiliar Package Manager" && exit 1
		fi
	}
}

install_ssl
clear

encode() {
	input="$1"
	output="$input.enc"
	openssl enc -aes-256-ecb -a -pbkdf2 -e -in "$input" -out "$output" -k "$2"
	[ -e "$output" ] && echo "[-] Output : " $output
	echo "[-] Passwd : " $3
}

decode() {
	input="$1"
	output="${input%.*}"
	openssl enc -aes-256-ecb -a -pbkdf2 -d -in "$input" -out "$output" -k "$2" 2>/dev/null
	[ $? != 0 ] && echo "[!] Wrong Password" && sleep 1 && rm -f "$output" && exit 1
	[ -e "$output" ] && echo -e "\n[-] Output : " $output
}

check_file() {
	file="$1$2"
	[ ! -e "$file" ] && {
		read -p "[-] Filename: " nname
		file="${nname}$2"
	}
	[ ! -e "$file" ] && echo "[!] No such files" && sleep 1 && exit 1
	filename="$file"
}

passwrd() {
	[ "$1" != '' ] && {
		hash_pass=$(echo -n $1 | base64 | sha256sum | awk '{print $1}')
	} || {
		echo "[!] Password can't be empty" && exit 1
	}
}

main_menu() {
	read -n1 -p "[-] Select an Option [d|e] " enc_dec
	echo
	case $enc_dec in
		[dD])
			check_file "$1" ".7z.enc" # encoded extension
			read -sp "[-] Password: " typedpass
			echo
			passwrd "$typedpass"
			decode "$filename" "$hash_pass"
			;;
		[eE])
			check_file "$1" ".7z" # base extension
			read -p "[-] Password: " typedpass
			echo
			passwrd "$typedpass"
			encode "$filename" "$hash_pass" "$typedpass"
			;;
		*)
			echo "[!] Input d or e" && sleep 1 && exit 1
			;;
	esac
}

main_menu "data" # File Name (data.7z)
