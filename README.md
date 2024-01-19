High-level approach:
The code establishes a socket connection with a server and communicates using a JSON-based protocol.
It implements a basic Wordle solver that guesses words based on feedback received from the server.
The guessing strategy involves filtering a word list based on the hints received for previous guesses.

Challenges faced:
Recognizing the wordle game edge cases where if my wordle solver guesses a word that contains a duplicate
letter, the hint received can be situational based on the correct word. Had to handle the duplicate letter
edge case. Also needed to make sure I receive a complete message from the server. 
Overcame this challenge by reading from the socket until I receive a newline (\n)

Guessing strategy:
The program uses a simple strategy to filter the word list based on the hint ex:"00000" received for each guess.
It maintains a list of possible words: "words_to_list" and updates it after each guess, 
narrowing down the options based on the feedback. It repeats this process until the server sends me a bye message 
to confirm the correct word is guessed. For example if the input was "01000", then we would filter the 
words_to_list by overwriting the list to only contain words that contain the letter at index[1] where the 
integer 1 is in the input. If the hint was "02000", then it would filter words that have the letter
at index[1] since it is in the correct position. It repeats this process until the word list reduces to a size of
1 which means it has found the correct guess. The server must send a 'bye' message at this point and we retrieve
the secret flag.


Testing overview:
Ran the client program and tested by handling errors or exceptions during the socket communication with try
and except exceptions. Testing would involve running the code against a server and observing its behavior 
during the Wordle game and I would catch specific exception handing messages to make sure my code is functional
Tested my wordle solver algorithm using python unit testing. Makes sure my list is correctly optmizing and filtering
according to my helper methods. 

