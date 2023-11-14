# Plant Protocol
Client-server project for ECE:3540 Communication Networks.

## How to Setup
1. Download the repository files
2. First, run the server (`py server.py`)
3. Next, run the client (`py client.py`)
5. In the client terminal, enter the servers IP address
6. In the client terminal, create a username

## How to Play
1. Filter though your plants by pressing the displayed arrows
2. Your plant hunger increases with time, press 'f' to feed
3. Your plant thirst increases with time, press 'w' to water
4. You make money every second, buy new plants by pressing the "New Plant" button
5. 




### To-Do:
- [ ] Server program file(s)
    - [x] Set up base connection between server and client 
    - [x] Create database (probably a JSON file)
    - [x] send data to client
    - [x] receive data from client and write to database
- [ ] Client program file(s)
    - [x] Set up base connection between client and server
    - [x] send data to server
    - [x] receive data from server
    - [x] make changes accordingly
    - [ ] User Interface
- [ ] Protocol Documentation
    - [ ] (5 pts) General introduction for the designed protocol. Should mention whether it uses TCP or UDP as the transport layer service and why.
    - [x] (10 pts) Header fields should be included in message formatting. Explicitly list the formatting for the server, client, and handshaking process if they use different formats. Explain each field in the message format.
    - [x] Application Layer handshaking process (NOTE: This is NOT the TCP handshaking)
    - [ ] How this protocol works after hand-shaking process. Use both description and figures to help readers to understand the process. Note: A good protocol should handle all unexpected/imperfect situations. For example, what happens after receiving a packet with the wrong format? Any mechanism to check/avoid corrupted packets? etc.
- [ ] README file
    - [ ] should thoroughly explain how to run both the client and the server