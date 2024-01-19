import socket
import json
import argparse
import ssl
import os
import random


# Initialize word list
current_directory = os.getcwd()
file = open("wordlist.txt", "r")
words = file.read()
# Word list in list form
words_to_list = words.split("\n")
file.close()


parser = argparse.ArgumentParser()

parser.add_argument('-p', '--port', type=int, default=27993, help='Port to listen on')
parser.add_argument('-s', '--secure', action='store_true', help='Use SSL')
parser.add_argument('hostname', type=str, help='Hostname to connect to')
parser.add_argument('username', type=str, help='Username to')
command = parser.parse_args()

HOST = command.hostname
PORT = command.port
SECURE = command.secure

if command.port == 27993 and command.secure is True:
    PORT = 27994



# Create a socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Check connection type
if SECURE:
    context = ssl.create_default_context()
    socket = context.wrap_socket(socket, server_hostname=HOST)

# connect to server
socket.connect((HOST, PORT))

# hello message
hello_message = {
    "type": "hello",
    "northeastern_username": command.username
}

# send hello message to server
socket.sendall(json.dumps(hello_message).encode() + b'\n')

# Receive data from the server until \n is detected
received_data = b''
while True:
    message = socket.recv(1024)
    if not message:
        break
    received_data += message
    if b'\n' in message:
        break

# get reply from server
start_data = received_data.decode().strip()
start_message = json.loads(start_data)

# store game ID
GAME_ID = start_message.get("id")


# Wordle solver implementation

def filter_words_no_letter(wordList, letter):
    emptyList = []
    for everyword in wordList:

        if letter not in everyword:
            emptyList.append(everyword)
    return emptyList


def filter_words_with_letter(wordList, letter):
    emptyList = []
    for everyword in wordList:
        if letter in everyword:
            emptyList.append(everyword)
    return emptyList

def filter_words_wrong_position(wordList, index, letter):
    emptyList = []
    for everyword in wordList:
        if letter != everyword[index]:
            emptyList.append(everyword)
    return emptyList

def filter_words_correct_position(wordList, index, letter):
    emptyList = []
    for everyword in wordList:
        if letter == everyword[index]:
            emptyList.append(everyword)
    return emptyList


def contains_duplicate_letter(word, index):
    for i in range(len(word)):
        if i != index and word[i] == word[index]:
            return True
    return False


def grey_all_duplicates(word, letter, userinput):
    for i in range(5):
        if word[i] == letter and userinput[i] != '0':
            return False
    return True


def analyze_result(wordUsed, userInput, wordList):
    index = 0
    number = ''.join(str(x) for x in userInput)
    for element in number:
        emptylist = []
        if element == '0':
            if not contains_duplicate_letter(wordUsed, index):
                newlist = filter_words_no_letter(wordList, wordUsed[index])
                for newword in newlist:
                    emptylist.append(newword)
            else:
                if grey_all_duplicates(wordUsed, wordUsed[index], userInput):
                    newlist = filter_words_no_letter(wordList, wordUsed[index])
                    for newword in newlist:
                        emptylist.append(newword)
                else:
                    for newword in wordList:
                        emptylist.append(newword)
        if element == '1':
            newlist = filter_words_with_letter(wordList, wordUsed[index])
            for newword in newlist:
                emptylist.append(newword)

            newsecondlist = filter_words_wrong_position(emptylist, index, wordUsed[index])
            emptylist.clear()
            for posiword in newsecondlist:
                emptylist.append(posiword)

        if element == '2':
            newlist = filter_words_correct_position(wordList,index, wordUsed[index])
            for newword in newlist:
                emptylist.append(newword)

        wordList.clear()
        for everyword in emptylist:
            wordList.append(everyword)

        index += 1
    return wordList


def get_guess(userInput, wordlist, word):
    startWord = word
    optimizedList = analyze_result(startWord, userInput, wordlist)
    return optimizedList

def send_guess(GAME_ID, word):
    guess_message = {
        "type": "guess",
        "id": GAME_ID,
        "word": word
    }

    # send hello message to server
    socket.sendall(json.dumps(guess_message).encode() + b'\n')

    # Receive data from the server until \n is detected
    received_data = b''
    while True:
        message = socket.recv(1024)
        if not message:
            break
        received_data += message
        if b'\n' in message:
            break

    # get reply from server
    start_data = received_data.decode().strip()
    start_message = json.loads(start_data)
    return start_message


# Retrieves flag with while loop
MESSAGE_TYPE = ''
FLAG = ''
while MESSAGE_TYPE != 'bye':
    message = send_guess(GAME_ID, random.choice(words_to_list))
    if message["type"] == 'bye':
        print(message["flag"])
        break
    guesses = message["guesses"][-1]
    hint = guesses["marks"]
    wordused = guesses["word"]
    stringhint = ""
    for number in hint:
        stringhint += str(number)
    GAME_ID = message["id"]
    optimizedlist = get_guess(hint, words_to_list, wordused)
    words_to_list = optimizedlist







