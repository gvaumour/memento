# Memento 


Display a few picto, the player must find the only one that is displayed on the matrix on buttons in front of him
It interacts with a centralized server that sends json requests through websockets that start and stop the game

# Installation 

*Game engine:*
The script runs with python3-8-10, the game engine use the pyglet package v1.5.21
````
pip3 install pyglet 
````

*Web socket Management:*
The websocket service is managed with the [websocat][2] project: 

It receives data from a web socket and print it in stdout as text
You need to download the builtin version you need based on the platform it is run on. 
For raspberry, the linuxarm32 is available [here][1], the v1.9.0 is used for the project


# Run 

# Changelog

* First release v1: 28/01/2022


Author: Gregory Vamourin 

[1]: https://github.com/vi/websocat/releases/download/v1.9.0/websocat_linuxarm32
[2]: https://github.com/vi/websocat/releases
