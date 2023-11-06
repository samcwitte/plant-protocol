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

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plant Protocol")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'water-icon.png')))
clock = pygame.time.Clock()
running = True

SCALE_FACTOR = 4
stage_num = 1

# NOTE: ALL PLANT SPRITES SHOULD BE 32x32 AND A .PNG FILE
pot_image = pygame.image.load(os.path.join('assets', 'pot.png')).convert_alpha()
pot_image = pygame.transform.scale(pot_image, (pot_image.get_width() * SCALE_FACTOR, pot_image.get_height() * SCALE_FACTOR))
pot_rect = pot_image.get_rect()
pot_rect.center = (center_x, center_y)
pot_rect.bottom = SCREEN_HEIGHT - pot_image.get_height()/2 + 30

pot_shadow_image = pygame.image.load(os.path.join('assets', 'pot_shadow.png')).convert_alpha()
pot_shadow_image = pygame.transform.scale(pot_shadow_image, (pot_shadow_image.get_width() * SCALE_FACTOR, pot_shadow_image.get_height() * SCALE_FACTOR))
pot_shadow_rect = pot_shadow_image.get_rect()
pot_shadow_rect.center = (pot_rect.centerx + (13 * SCALE_FACTOR), pot_rect.bottom + (1 * SCALE_FACTOR))

plant_image = pygame.image.load(os.path.join('assets', 'myrtillocactus-geometrizans', 'stage1.png')).convert_alpha()
plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))
plant_rect = plant_image.get_rect()
plant_rect.center = (center_x, center_y)
plant_rect.bottom = pot_rect.centery - (10 * SCALE_FACTOR)

table_image = pygame.image.load(os.path.join('assets', 'table.png')).convert_alpha()
table_image = pygame.transform.scale(table_image, (table_image.get_width() * SCALE_FACTOR, table_image.get_height() * SCALE_FACTOR))
table_rect = table_image.get_rect()
table_rect.center = (center_x, center_y)
table_rect.bottom = SCREEN_HEIGHT

greenhouse_image = pygame.image.load(os.path.join('assets', 'greenhouse-background.png')).convert_alpha()
greenhouse_image = pygame.transform.scale(greenhouse_image, (greenhouse_image.get_width() * SCALE_FACTOR, greenhouse_image.get_height() * SCALE_FACTOR))
greenhouse_rect = greenhouse_image.get_rect()
greenhouse_rect.center = (center_x, center_y)

arrow_next_image = pygame.image.load(os.path.join('assets', 'arrow-next.png')).convert_alpha()
arrow_next_image = pygame.transform.scale(arrow_next_image, (arrow_next_image.get_width() * SCALE_FACTOR, arrow_next_image.get_height() * SCALE_FACTOR))
arrow_next_rect = arrow_next_image.get_rect()
arrow_next_rect.center = (center_x + (SCREEN_WIDTH//2) - (6 * SCALE_FACTOR), center_y)

arrow_prev_image = pygame.image.load(os.path.join('assets', 'arrow-next.png')).convert_alpha()
arrow_prev_image = pygame.transform.scale(arrow_prev_image, (arrow_prev_image.get_width() * SCALE_FACTOR, arrow_prev_image.get_height() * SCALE_FACTOR))
arrow_prev_image = pygame.transform.flip(arrow_prev_image, 1, 0)
arrow_prev_rect = arrow_prev_image.get_rect()
arrow_prev_rect.center = (center_x - (SCREEN_WIDTH//2) + (6 * SCALE_FACTOR), center_y)

banner_image = pygame.image.load(os.path.join('assets', 'banner.png')).convert_alpha()
banner_image = pygame.transform.scale(banner_image, (banner_image.get_width() * SCALE_FACTOR, banner_image.get_height() * SCALE_FACTOR))
banner_rect = banner_image.get_rect()
banner_rect.center = (center_x, banner_image.get_height()//2)


# Main game loop
while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # Load the new plant image (make sure this file exists)
                stage_num += 1
                if stage_num > 5: stage_num = 1
            if event.key == pygame.K_LEFT:
                stage_num -= 1
                if stage_num < 1: stage_num = 5
            new_plant_image_path = os.path.join('assets', 'myrtillocactus-geometrizans', 'stage' + str(stage_num) + '.png')
            plant_image = pygame.image.load(new_plant_image_path).convert_alpha()
            plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))
            # Update the rect to match the new image
            plant_rect.center = (center_x, center_y)
            plant_rect.bottom = pot_rect.centery - (10 * SCALE_FACTOR)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                # Check if mouse position is over the sprite
                if arrow_next_rect.collidepoint(mouse_pos):
                    print("> Next arrow left-clicked!")
                if arrow_prev_rect.collidepoint(mouse_pos):
                    print("> Prev arrow left-clicked!")
                
            if event.button == 3:
                print("> Right click!")


    # fill the screen with a color to wipe away anything from last frame
    # draws from back to front
    screen.fill(pygame.color.Color(132, 197, 255, 255))
    screen.blit(greenhouse_image, greenhouse_rect)
    screen.blit(table_image, table_rect)
    screen.blit(pot_shadow_image, pot_shadow_rect)
    screen.blit(pot_image, pot_rect)
    screen.blit(plant_image, plant_rect)
    
    # Banner section
    screen.blit(banner_image, banner_rect)
    # screen.blit(currency_image, currency_rect)
    
    screen.blit(arrow_next_image, arrow_next_rect)
    screen.blit(arrow_prev_image, arrow_prev_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()