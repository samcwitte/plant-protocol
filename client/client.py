import socket
import os, sys
import pygame
import easygui
import time
import json
import random

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from lib import packets

PORT = 65432 # This needs to match the server's port.

def getNewPlant():
    global plants
    newPlant = plants[random.randint(0,len(plants) - 1)]
    return newPlant

def getPlantLevel():
    global user_plants, currentPlantIndex
    plantLevel = (int(user_plants[currentPlantIndex]['xp']) // 10) + 1 # can't be level 0
    return max(1, min(plantLevel, 5)) # clamps the level between 1 and 5 (incl.)

def nextPlant():
    global user_plants, currentPlantIndex, plant_image, water_level, food_level
    if currentPlantIndex == len(user_plants) - 1: # max index
        currentPlantIndex = 0
    else:
        currentPlantIndex += 1
    levelString = 'stage' + str(getPlantLevel()) + '.png'
    plant_image = pygame.image.load(os.path.join('assets', 'sprites', user_plants[currentPlantIndex]['sciname'].lower().replace(' ', '-'), levelString)).convert_alpha()
    plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))

    water_level = getWaterLevel()
    food_level = getFoodLevel()

def prevPlant():
    global user_plants, currentPlantIndex, plant_image, water_level, food_level
    if currentPlantIndex == 0: # min index
        currentPlantIndex = len(user_plants) - 1
    else:
        currentPlantIndex -= 1
    levelString = 'stage' + str(getPlantLevel()) + '.png'
    plant_image = pygame.image.load(os.path.join('assets', 'sprites', user_plants[currentPlantIndex]['sciname'].lower().replace(' ', '-'), levelString)).convert_alpha()
    plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))

    water_level = getWaterLevel()
    food_level = getFoodLevel()

def getWaterDecayRate():
    global user_plants, currentPlantIndex
    return user_plants[currentPlantIndex]["water_decay_rate"]

def getFoodDecayRate():
    global user_plants, currentPlantIndex
    return user_plants[currentPlantIndex]["food_decay_rate"]

def getLastWater():
    global user_plants, currentPlantIndex
    return user_plants[currentPlantIndex]["last_water"]

def getLastFeed():
    global user_plants, currentPlantIndex
    return user_plants[currentPlantIndex]["last_feed"]

def getWaterLevel():
    global user_plants, currentPlantIndex, water_level
    water = round(user_plants[currentPlantIndex]["water"] - ((time.time() - getLastWater()) * (getWaterDecayRate()/100)), 0)
    if water < 0: water = 0
    water_level = water
    return water

def getFoodLevel():
    global user_plants, currentPlantIndex, food_level
    food = round(user_plants[currentPlantIndex]["food"] - ((time.time() - getLastFeed()) * (getFoodDecayRate()/100)), 0)
    if food < 0: food = 0
    food_level = food
    return food

def getMoneyRate():
    global user_plants, currentPlantIndex
    return user_plants[currentPlantIndex]["money_rate"]

def decreaseWaterLevel():
    global user_plants, currentPlantIndex, water_level
    water_level -= user_plants[currentPlantIndex]["water_decay_rate"]
    # user_plants[currentPlantIndex]['water'] -= user_plants[currentPlantIndex]["water_decay_rate"]
    if water_level < 0: water_level = 0
    water_level = round(water_level, 1)

    user_plants[currentPlantIndex]["water"] = water_level

    print(f"\n\nWATER LEVEL | {water_level}")

def decreaseFoodLevel():
    global user_plants, currentPlantIndex, food_level
    food_level -= user_plants[currentPlantIndex]["food_decay_rate"]
    if food_level < 0: food_level = 0
    food_level = round(food_level, 1)

    user_plants[currentPlantIndex]["food"] = food_level

    print(f"FOOD LEVEL | {food_level}")           
            
def increaseWaterLevel():
    global water_level, last_water
    water_level += 10
    if water_level > 100: water_level = 100 
    last_water = time.time()

    user_plants[currentPlantIndex]["water"] = water_level
    user_plants[currentPlantIndex]["last_water"] = last_water

def increaseFoodLevel():
    global food_level, last_feed
    food_level += 5
    if food_level > 100: food_level = 100
    last_feed = time.time()

    user_plants[currentPlantIndex]["food"] = food_level
    user_plants[currentPlantIndex]["last_feed"] = last_feed


os.system("cls")

#IP Handling
print("Input IP to connect to (leave blank for localhost)")
ip_addr = input("> ")
if not ip_addr:
    ip_addr = "127.0.0.1"

# Username handling
print("Username (must be between 3 and 16 characters long)")
username = input("> ")
if (len(username) > 16 or len(username) < 3):
    print("Username must be between 3 and 16 characters.")
    quit()

# Create a new socket using IPv4 (AF_INET) and TCP protocol (SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Establish a connection to the specified server (HOST and PORT).
    try:
        s.connect((ip_addr, PORT))
    except BlockingIOError:
        # Non-blocking mode connection will not be established immediately
        pass

    # 1) Send a byte-string message "ICON" to the server.
    ICON = packets.Packet("ICON", username, "")
    s.sendall(packets.Packet.toBytes(ICON))
    
    # 2) Wait for "ICON" response from the server and receive up to 1024 bytes of data.
    while True:
        try:
            packet = s.recv(2048)
            if packet:                
                # 3) Check that the first packet received is an ICON packet.
                decoded_packet = packets.Packet.fromBytes(packet)
                if (decoded_packet[2] == "ICON"):
                    print("RECV | ICON | Connection is a go.")
                    pass
                else:
                    what_packet = packets.Packet("WHAT", "", "")
                    s.sendall(packets.Packet.toBytes(what_packet))
                    print("SEND | WHAT")
                break
            
        except socket.error as oops:
            print("ERROR 1: " + oops)
            time.sleep(0.1)
            continue
    
    # 4) Send data request packet
    data_request = packets.Packet("REQD", username, "USER")
    s.sendall(packets.Packet.toBytes(data_request))
    print("SEND | REQD")
    
    # 5) Wait for server response
    while True:
        try:
            packet = s.recv(2048)
            if packet:
                
                decoded_packet = packets.Packet.fromBytes(packet)
                if decoded_packet[2] == "DATA":
                    print("RECV | DATA | " + str(decoded_packet))
                    
                    # Set game variables from received data
                    gamedata = json.loads(decoded_packet[4]) # might not work
                    # print(str(gamedata))
                    
                    # Constructs Payload ACK packet and sends it
                    ack_packet = packets.Packet("DACK", "", "")
                    s.sendall(packets.Packet.toBytes(ack_packet))
                    print("SEND | DACK")
                    # put JSON fuckery here
                
                else:
                    WHAT = packets.Packet("WHAT", "", "")
                    s.sendall(packets.Packet.toBytes(WHAT))
                    print("SEND | WHAT")
                break
                    
        except socket.error as oops:
            print("ERROR 2: " + str(oops))
            time.sleep(0.1)
            continue
        
    plant_data_request = packets.Packet("REQD", username, "PLANTS")
    s.sendall(packets.Packet.toBytes(plant_data_request))
    print("SEND | REQD")
    
    # 5) Wait for server response
    while True:
        try:
            packet = s.recv(2048)
            if packet:
                
                decoded_packet = packets.Packet.fromBytes(packet)
                if decoded_packet[2] == "DATA":
                    print("RECV | DATA | " + str(decoded_packet))
                    
                    # Set game variables from received data
                    plants = json.loads(decoded_packet[4]) # might not work
                    # print(str(gamedata))
                    
                    # Constructs Payload ACK packet and sends it
                    ack_packet = packets.Packet("DACK", "", "")
                    s.sendall(packets.Packet.toBytes(ack_packet))
                    print("SEND | DACK")
                    # put JSON fuckery here
                
                else:
                    WHAT = packets.Packet("WHAT", "", "")
                    s.sendall(packets.Packet.toBytes(WHAT))
                    print("SEND | WHAT")
                break
                    
        except socket.error as oops:
            print("ERROR 3: " + str(oops))
            time.sleep(0.1)
            continue


    ##################################### Pygame setup #####################################
    pygame.init()
    pygame.font.init()
    ui_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Minecraftia-Regular.ttf'), 28) # use for UI elements such as money, etc.
    sciname_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Minecraftia-Regular.ttf'), 14)
    realname_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Minecraftia-Regular.ttf'), 18)
    nickname_font = pygame.font.Font(os.path.join('assets', 'fonts', 'Minecraftia-Regular.ttf'), 20)
    long_text_font = pygame.font.SysFont('Helvetica', 16) # use for long text descriptions
    
    ui_text_color = (0, 0, 0)
    sciname_color = (0, 0, 0)
    realname_color = (30, 30, 30)
    long_text_color = (255, 255, 127)
    nickname_color = (0, 0, 0)

    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 600

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Plant Protocol")
    pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'sprites', 'water-icon.png')))

    # Set up colors
    water_button_color = (0, 148, 255)

    # Set up button properties
    button_width, button_height = 60, 25
    water_button_x, water_button_y = (15) , (500)

    food_button_color = (255,255,0)
    food_button_x, food_button_y = (230) , (500)

    color = (0,0,0)
    clock = pygame.time.Clock()
    running = True

    SCALE_FACTOR = 4
    
    user_plants = gamedata['plants']
    
    # god of the game
    currentPlantIndex = 0

    # NOTE: ALL PLANT SPRITES SHOULD BE 32x32 AND A .PNG FILE
    if True: # This does nothing. This is so I can minimize the sprites section of code.
        pot_image = pygame.image.load(os.path.join('assets', 'sprites', 'pot.png')).convert_alpha()
        pot_image = pygame.transform.scale(pot_image, (pot_image.get_width() * SCALE_FACTOR, pot_image.get_height() * SCALE_FACTOR))
        pot_rect = pot_image.get_rect()
        pot_rect.center = (center_x, center_y)
        pot_rect.bottom = SCREEN_HEIGHT - pot_image.get_height()/2 + 30

        pot_shadow_image = pygame.image.load(os.path.join('assets', 'sprites', 'pot_shadow.png')).convert_alpha()
        pot_shadow_image = pygame.transform.scale(pot_shadow_image, (pot_shadow_image.get_width() * SCALE_FACTOR, pot_shadow_image.get_height() * SCALE_FACTOR))
        pot_shadow_rect = pot_shadow_image.get_rect()
        pot_shadow_rect.center = (pot_rect.centerx + (13 * SCALE_FACTOR), pot_rect.bottom + (1 * SCALE_FACTOR))

        levelString = 'stage' + str(getPlantLevel()) + '.png'
        plant_image = pygame.image.load(os.path.join('assets', 'sprites', user_plants[0]['sciname'].lower().replace(' ', '-'), levelString)).convert_alpha()
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

        water_button_text = long_text_font.render('Water' , True , color)
        food_button_text = long_text_font.render('Feed', True, color)

    # TODO CHANGE ME TO UPDATE FROM SERVER'S VALUE
    time_elapsed = 0
    user_balance = int(gamedata['balance'])
    active_plant_index = 0
    
    # Font surface setup
    balance_surface = ui_font.render(str(user_balance), False, ui_text_color)
    realname_surface = realname_font.render(str(user_plants[currentPlantIndex]['realname']), False, realname_color)
    sciname_surface = sciname_font.render(str(user_plants[currentPlantIndex]['sciname']), False, sciname_color)
    nickname_surface = nickname_font.render(str(user_plants[currentPlantIndex]['nickname']), False, nickname_color)

    # water and food decay
    water_decay_rate = getWaterDecayRate()
    food_decay_rate = getFoodDecayRate()

    # current water and food levels (percentage 0%-100%)
    water_level = getWaterLevel()
    food_level = getFoodLevel()

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Set gamedata variable here to send back to server
                gamedata['balance'] = user_balance

                # plant info dump
                gamedata['plants'] = user_plants
                                
                while True:
                    try:
                        DATA = packets.Packet("DATA", username, json.dumps(gamedata))
                        s.sendall(packets.Packet.toBytes(DATA))
                        print("SEND | DATA")
                        time.sleep(0.1)
                        
                        packet = s.recv(2048)
                        if packet:
                            # 3) Check that the first packet received is an ICON packet.
                            decoded_packet = packets.Packet.fromBytes(packet)
                            if (decoded_packet[2] == "DACK"):
                                print("RECV | DACK | Server sent acknowledgement of received game data.")
                                break
                            else:
                                raise Exception("DACK not received")
                    except socket.error as oops:
                        print("ERROR \"1\": " + str(oops))
                        time.sleep(0.1)
                        continue
                
                # Send DONE Packet
                DONE = packets.Packet("DONE", username, "")
                s.sendall(packets.Packet.toBytes(DONE))
                print("SEND | DONE")
                running = False

            if event.type == pygame.KEYDOWN:
                match event.key:

                    case pygame.K_p:
                        if (user_balance >= 500):
                            user_balance -= 500
                            user_plants.append(getNewPlant())

                    case pygame.K_w:
                        # add to the water level, cannot go above 100
                        increaseWaterLevel()

                    case pygame.K_f:
                        # add to the food level, cannot go above 100
                        increaseFoodLevel()

                #new_plant_image_path = os.path.join('assets', 'dracaena-sanderiana', 'stage' + str(stage_num) + '.png')
                #new_plant_image_path = os.path.join('assets', 'sprites', gamedata['plants'][active_plant_index]['picture_path'], 'stage' + str(stage_num) + '.png')
                #plant_image = pygame.image.load(new_plant_image_path).convert_alpha()
                #plant_image = pygame.transform.scale(plant_image, (plant_image.get_width() * SCALE_FACTOR, plant_image.get_height() * SCALE_FACTOR))
                ## Update the rect to match the new image
                #plant_rect.center = (center_x, center_y)
                #plant_rect.bottom = pot_rect.centery - (10 * SCALE_FACTOR)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    # Check if mouse position is over the sprite
                    if arrow_next_rect.collidepoint(mouse_pos):
                        # print("> Next arrow left-clicked!")
                        nextPlant()
                        
                    if arrow_prev_rect.collidepoint(mouse_pos):
                        # print("> Prev arrow left-clicked!")
                        prevPlant()
                        
                    if shop_rect.collidepoint(mouse_pos):
                        print("> Shop is coming soon!")
                        # TODO IMPLEMENT SHOP
                        
                    if settings_rect.collidepoint(mouse_pos):
                        print("> Settings are coming soon!")
                        # TODO IMPLEMENT SETTINGS PANEL
                    
                    if plant_rect.collidepoint(mouse_pos):
                        user_plants[currentPlantIndex]['xp'] = str(int(user_plants[currentPlantIndex]['xp']) + 2)
                        nextPlant()
                        prevPlant()
                        
                    nickname_rect = nickname_surface.get_rect()
                    nickname_rect.centerx = center_x
                    nickname_rect.centery = 0.92*SCREEN_HEIGHT - 20 + (nickname_rect.height//2)
                    if nickname_rect.collidepoint(mouse_pos):
                        user_plants[currentPlantIndex]['nickname'] = easygui.enterbox("New plant name: ")
                    
                if event.button == 3:
                    print("> Right click!")
        
        dt = clock.tick(60)
        money_rate = getMoneyRate()
        # money_rate = sum of all plants' money rates
        
        balance_surface = ui_font.render(str(user_balance), False, ui_text_color)
        realname_surface = realname_font.render(str(user_plants[currentPlantIndex]['realname']), False, realname_color)
        sciname_surface = sciname_font.render(str(user_plants[currentPlantIndex]['sciname']), False, sciname_color)
        nickname_surface = nickname_font.render(str(user_plants[currentPlantIndex]['nickname']), False, nickname_color)
        
        # Plant money update logic here
        if (time_elapsed >= 1000):

            # update user balance
            user_balance += money_rate # TODO CHANGE ME

            decreaseWaterLevel()
            decreaseFoodLevel()

            # reset elapsed time
            time_elapsed = 0

        color = (255,255,0)
        pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))
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
        
        # Plant stats icons
        screen.blit(water_image, water_rect)
        screen.blit(food_image, food_rect)
        
        # Next/Prev plant arrows
        screen.blit(arrow_next_image, arrow_next_rect)
        screen.blit(arrow_prev_image, arrow_prev_rect)

        screen.blit(sciname_surface, (center_x - sciname_font.size(str(user_plants[currentPlantIndex]['sciname']))[0]//2, 0.92*SCREEN_HEIGHT + 20))
        screen.blit(realname_surface, (center_x - realname_font.size(str(user_plants[currentPlantIndex]['realname']))[0]//2, 0.92*SCREEN_HEIGHT))
        screen.blit(nickname_surface, (center_x - nickname_font.size(str(user_plants[currentPlantIndex]['nickname']))[0]//2, 0.92*SCREEN_HEIGHT - 20))

        pygame.draw.rect(screen, water_button_color, (water_button_x, water_button_y, button_width, button_height))
        pygame.draw.rect(screen, food_button_color, (food_button_x, food_button_y, button_width, button_height))
        
        screen.blit(water_button_text , (30,503))
        screen.blit(food_button_text , (245,503))
        # flip() the display to put your work on screen
        pygame.display.flip()

        time_elapsed += dt
    
    pygame.quit()