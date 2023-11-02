import socket
import os, sys
import pygame

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets

HOST = "127.0.0.1"
PORT = 65432 # This needs to match the server's port.

os.system("cls") # clears the console
# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Establish a connection to the specified server (HOST and PORT).
    s.connect((HOST, PORT))
    # Send a byte-string message "ICON" to the server.
    s.sendall("ICON".encode('utf-8'))
    # Wait for a response from the server and receive up to 1024 bytes of data.
    data = s.recv(1024)

# Print the data received from the server.
formatted_data = str(data.decode('utf-8')).split("\n")
for i in formatted_data:
    if len(i) > 24:
        packets.Packet.summary(i)
        
# To wrap up...
# Client sends "DONE {modified_dictionary}" 
# Server receives it, tries to modify the database.
#   if failure, send "BAD" or something
#   if success, send "DONE"
# client closes connections


# To send data...
# s.sendall(packet_to_send.toBytes()) 







##################################### Pygame setup #####################################
pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

SCALE_FACTOR = 4

pot_image = pygame.image.load(os.path.join('assets/pot.png')).convert_alpha()
pot_image = pygame.transform.scale(pot_image, (pot_image.get_width() * SCALE_FACTOR, pot_image.get_height() * SCALE_FACTOR))

pot_rect = pot_image.get_rect()

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2   

pot_rect.center = (center_x, center_y)

pygame.transform.scale()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    screen.blit(pot_image, pot_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()