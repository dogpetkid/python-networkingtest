# python-networkingtest
Testing sockets to work inside another modules to use in a turn-based game

## Client and Server test
The server and client side (tests) are meant to be used together. To get the 2 to connect, change the HOST string to be the IP printed by the other computer.
### Uses
* Sends messages from client to server (when running __main__).
* Has the error and functions to communicate be client and server and to package and unpackage arrays.

## Client and Server arraytest
Useless test file as a proof of concept to send arrays.
### Uses
* Proves the concept of sending an array as a string and then extracting the array from the string again.
* Sends array from client to server.

## Hybrid test
A file proving a turn based chat.
### Uses
* Proves sending data both ways on a socket connection.
* Choose between host or client connection.
* Turn based "chat" sending strings.

## Choose
Simple hand-written module to force a user to choose only what is in a list of choices.
### Uses
* Module that returns a choice from the user that they get from a  list.

## Chess
Hand-written code to play chess.
### Uses
* Plays chess heavily focused on the object oriented part of python.
* Has a board with pieces that 'move' themselves from user input.
* Has multiplayer compatibility (since v0.1.0).
