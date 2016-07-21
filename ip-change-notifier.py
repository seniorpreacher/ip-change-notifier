#!/usr/bin/python3

import json
import subprocess
import smtplib
from email.mime.text import MIMEText


def run(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = process.stderr.decode("utf-8")  # returning the stderr text, if any
    if len(error) > 0:
        raise ValueError(error)
    return process.stdout.decode("utf-8").strip()

ip_file_path = 'ip_info.txt'

def get_old_ip():
    old_ip = None
    try:
        with open(ip_file_path, 'r') as ip_file:
            return ip_file.readline().strip()
    except FileNotFoundError:
        with open(ip_file_path, 'w') as ip_file:
            ip_file.write(ip)

def write_ip(ip):
    with open(ip_file_path, 'w') as ip_file:
        ip_file.write(ip)

def send_mail(ip, address):
    hostname = run(['hostname'])
    msg = MIMEText(hostname + ' just got a new IP address: ' + ip)
    msg['subject'] = 'New IP on ' + hostname
    msg['from'] = run(['whoami']) + '@' + hostname
    msg['to'] = address

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

def main():
    ifconfig_line = run(["ifconfig", "enp0s25"]).split('\n')[1]
    ifconfig_temp1 = ifconfig_line[ifconfig_line.find('inet addr') + 10:]
    current_ip = ifconfig_temp1[:ifconfig_temp1.find(' ')]

    try:
        old_ip = get_old_ip()
        if old_ip != current_ip:
            send_mail(current_ip, 'daniel.salamon@codecool.com')
            write_ip(current_ip)
    except FileNotFoundError:
        write_ip(current_ip)

main()
