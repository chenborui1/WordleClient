import socket
import json
import argparse

parser = argparse.ArgumentParser(
    usage='./client <-p port> <-s> [hostname] [NEU ID]',
    description='Wordle Client'
    )
parser.add_argument('-p', '--port', type=int, default=27993)
parser.add_argument('-s', '--secure', action='store_true')
parser.add_argument('hostname', type=str)
parser.add_argument('username', type=str)
command = parser.parse_args()

print(command.port)




