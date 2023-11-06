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
pygame.font.init()
ui_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Minecraftia-Regular.ttf'), 30) # use for UI elements such as money, etc.
long_text_font = pygame.font.SysFont('Helvetica', 16) # use for long text descriptions
ui_text_color = (0, 0, 0)
long_text_color = (255, 255, 127)

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plant Protocol")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'sprites', 'water-icon.png')))
clock = pygame.time.Clock()
running = True

SCALE_FACTOR = 4

# NOTE: ALL PLANT SPRITES SHOULD BE 32x32 AND A .PNG FILE
pot_image = pygame.image.load(os.path.join('assets', 'sprites', 'pot.png')).convert_alpha()
pot_image = pygame.transform.scale(pot_image, (pot_image.get_width() * SCALE_FACTOR, pot_image.get_height() * SCALE_FACTOR))
pot_rect = pot_image.get_rect()
pot_rect.center = (center_x, center_y)
pot_rect.bottom = SCREEN_HEIGHT - pot_image.get_height()/2 + 30

pot_shadow_image = pygame.image.load(os.path.join('assets', 'sprites', 'pot_shadow.png')).convert_alpha()
pot_shadow_image = pygame.transform.scale(pot_shadow_image, (pot_shadow_image.get_width() * SCALE_FACTOR, pot_shadow_image.get_height() * SCALE_FACTOR))
pot_shadow_rect = pot_shadow_image.get_rect()
pot_shadow_rect.center = (pot_rect.centerx + (13 * SCALE_FACTOR), pot_rect.bottom + (1 * SCALE_FACTOR))

plant_image = pygame.image.load(os.path.join('assets', 'sprites', 'myrtillocactus-geometrizans', 'stage1.png')).convert_alpha()
plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))
plant_rect = plant_image.get_rect()
plant_rect.center = (center_x, center_y)
plant_rect.bottom = pot_rect.centery - (10 * SCALE_FACTOR)

table_image = pygame.image.load(os.path.join('assets', 'sprites', 'table.png')).convert_alpha()
table_image = pygame.transform.scale(table_image, (table_image.get_width() * SCALE_FACTOR, table_image.get_height() * SCALE_FACTOR))
table_rect = table_image.get_rect()
table_rect.center = (center_x, center_y)
table_rect.bottom = SCREEN_HEIGHT

greenhouse_image = pygame.image.load(os.path.join('assets', 'sprites', 'greenhouse-background.png')).convert_alpha()
greenhouse_image = pygame.transform.scale(greenhouse_image, (greenhouse_image.get_width() * SCALE_FACTOR, greenhouse_image.get_height() * SCALE_FACTOR))
greenhouse_rect = greenhouse_image.get_rect()
greenhouse_rect.center = (center_x, center_y)

arrow_next_image = pygame.image.load(os.path.join('assets', 'sprites', 'arrow-next.png')).convert_alpha()
arrow_next_image = pygame.transform.scale(arrow_next_image, (arrow_next_image.get_width() * SCALE_FACTOR, arrow_next_image.get_height() * SCALE_FACTOR))
arrow_next_rect = arrow_next_image.get_rect()
arrow_next_rect.center = (center_x + (SCREEN_WIDTH//2) - (6 * SCALE_FACTOR), center_y)

arrow_prev_image = pygame.image.load(os.path.join('assets', 'sprites', 'arrow-next.png')).convert_alpha()
arrow_prev_image = pygame.transform.scale(arrow_prev_image, (arrow_prev_image.get_width() * SCALE_FACTOR, arrow_prev_image.get_height() * SCALE_FACTOR))
arrow_prev_image = pygame.transform.flip(arrow_prev_image, 1, 0)
arrow_prev_rect = arrow_prev_image.get_rect()
arrow_prev_rect.center = (center_x - (SCREEN_WIDTH//2) + (6 * SCALE_FACTOR), center_y)

top_banner_image = pygame.image.load(os.path.join('assets', 'sprites', 'banner.png')).convert_alpha()
top_banner_image = pygame.transform.scale(top_banner_image, (top_banner_image.get_width() * SCALE_FACTOR, top_banner_image.get_height() * SCALE_FACTOR))
top_banner_rect = top_banner_image.get_rect()
top_banner_rect.center = (center_x, top_banner_image.get_height()//2)

sunshine_image = pygame.image.load(os.path.join('assets', 'sprites', 'money-icon.png')).convert_alpha()
sunshine_image = pygame.transform.scale(sunshine_image, (sunshine_image.get_width() * SCALE_FACTOR * 0.75, sunshine_image.get_height() * SCALE_FACTOR * 0.75))
sunshine_rect = sunshine_image.get_rect()
sunshine_rect.center = (top_banner_rect.centerx - (0.2*SCREEN_WIDTH), top_banner_rect.centery)

water_image = pygame.image.load(os.path.join('assets', 'sprites', 'water-icon.png')).convert_alpha()
water_image = pygame.transform.scale(water_image, (water_image.get_width() * SCALE_FACTOR / 2, water_image.get_height() * SCALE_FACTOR / 2))
water_rect = water_image.get_rect()
water_rect.center = (0.07 * SCREEN_WIDTH, top_banner_rect.bottom + 25)

food_image = pygame.image.load(os.path.join('assets', 'sprites', 'food-icon.png')).convert_alpha()
food_image = pygame.transform.scale(food_image, (food_image.get_width() * SCALE_FACTOR / 2, food_image.get_height() * SCALE_FACTOR / 2))
food_rect = food_image.get_rect()
food_rect.center = (water_rect.centerx, water_rect.centery + 30)

shop_image = pygame.image.load(os.path.join('assets', 'sprites', 'shop-icon.png')).convert_alpha()
shop_image = pygame.transform.scale(shop_image, (shop_image.get_width() * SCALE_FACTOR / 2.5, shop_image.get_height() * SCALE_FACTOR / 2.5))
shop_rect = shop_image.get_rect()
shop_rect.center = (sunshine_rect.left // 2, top_banner_rect.centery)

settings_image = pygame.image.load(os.path.join('assets', 'sprites', 'settings-icon.png')).convert_alpha()
settings_image = pygame.transform.scale(settings_image, (settings_image.get_width() * SCALE_FACTOR / 2.5, settings_image.get_height() * SCALE_FACTOR / 2.5))
settings_rect = settings_image.get_rect()
settings_rect.center = (SCREEN_WIDTH - sunshine_rect.left // 2, top_banner_rect.centery)




# TODO CHANGE ME TO UPDATE FROM SERVER'S VALUE
user_balance = 129.43
balance_surface = ui_font.render(str(user_balance), False, ui_text_color)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_1:
                    stage_num = 1
                case pygame.K_2:
                    stage_num = 2
                case pygame.K_3:
                    stage_num = 3
                case pygame.K_4:
                    stage_num = 4
                case pygame.K_5:
                    stage_num = 5
                case _:
                    stage_num = 1
            
            # new_plant_image_path = os.path.join('assets', 'dracaena-sanderiana', 'stage' + str(stage_num) + '.png')
            new_plant_image_path = os.path.join('assets', 'sprites', 'myrtillocactus-geometrizans', 'stage' + str(stage_num) + '.png')
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
                    # TODO: cycle through user plants here
                if arrow_prev_rect.collidepoint(mouse_pos):
                    print("> Prev arrow left-clicked!")
                    # TODO: reverse cycle through user plants here
                if shop_rect.collidepoint(mouse_pos):
                    print("> Shop left-clicked!")
                    # TODO IMPLEMENT SHOP
                if settings_rect.collidepoint(mouse_pos):
                    print("> Settings left-clicked!")
                    # TODO IMPLEMENT SETTINGS PANEL
                
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
    screen.blit(top_banner_image, top_banner_rect)
    screen.blit(sunshine_image, sunshine_rect)
    screen.blit(balance_surface, (sunshine_rect.centerx + 25, sunshine_rect.centery - ui_font.get_height()//2))
    screen.blit(shop_image, shop_rect)
    screen.blit(settings_image, settings_rect)
    
    screen.blit(water_image, water_rect)
    screen.blit(food_image, food_rect)
    
    screen.blit(arrow_next_image, arrow_next_rect)
    screen.blit(arrow_prev_image, arrow_prev_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits FPS to 60

pygame.quit()