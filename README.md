# Plant Protocol
Client-server project for ECE:3540 Communication Networks.

## How to use
1. Download the repository files
2. First, run the server (`py server.py`)
3. Next, run the client (`py client.py`)
4. You're done!

### To-Do:
- [ ] Server program file(s)
    - [x] Set up base connection between server and client 
    - [x] Create database (probably a JSON file)
    - [ ] send data to client
    - [x] receive data from client and write to database
- [ ] Client program file(s)
    - [x] Set up base connection between client and server
    - [ ] send data to server
    - [ ] receive data from server
    - [ ] make changes accordingly
    - [ ] User Interface
- [ ] Protocol Documentation
    - [ ] (5 pts) General introduction for the designed protocol. Should mention whether it uses TCP or UDP as the transport layer service and why.
    - [ ] (10 pts) Header fields should be included in message formatting. Explicitly list the formatting for the server, client, and handshaking process if they use different formats. Explain each field in the message format.
    - [ ] Application Layer handshaking process (NOTE: This is NOT the TCP handshaking)
    - [ ] How this protocol works after hand-shaking process. Use both description and figures to help readers to understand the process. Note: A good protocol should handle all unexpected/imperfect situations. For example, what happens after receiving a packet with the wrong format? Any mechanism to check/avoid corrupted packets? etc.
- [ ] README file
    - [ ] should thoroughly explain how to run both the client and the server