import socket
import json

host = 'proj1.3700.network'
port = 27993

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server

# Create a dictionary with the correct JSON format
data = {
    "type": "hello",
    "northeastern_username": 'chen.po-j'
}

string_data = json.dumps(data)
send_data = string_data.encode('utf-8')

client_socket.sendall(send_data)




