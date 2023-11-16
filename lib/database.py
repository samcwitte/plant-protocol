import json

# TO IMPLEMENT DATABASE CLASS INCLUDE... from lib.database import Database

class Database:
    def __init__(self):
        self.database_file = "database/database.json"
    
    # get full plant list (used for the store)  
    def getUsers(self):
        # load in the database
        with open(self.database_file, 'r') as file:
            database = json.load(file)

            return database["users"]

    # get full plant list (used for the store)
    def getPlants(self):
        # load in the database
        with open(self.database_file, 'r') as file:
            database = json.load(file)

            return database["plants"]

    # return user data... used in other getters
    def getUserData(self, username):
        # load in the database
        with open(self.database_file, 'r') as file:
            data = json.load(file)
        file.close()

        for user in data['users']:
            if user['username'] == username:
                return user['user_data']

        return None

    # get user money balance
    def getBalance(self, username):
        user_data = self.getUserData(username)
        if user_data:
            return user_data.get('balance', None)
        return None
    
    # get user plants
    def getUserPlants(self, username):
        user_data = self.getUserData(username)
        if user_data:
            return user_data["plants"]
        return []

    # get one of the users plants
    def getSingleUserPlant(self, username, scientific_name):
        plants = self.getUserPlants(username)
        for plant in plants:
            if plant["sciname"] == scientific_name:
                return plant
        return None # aint got that plant 
    
    def createNewUser(self, username):
        with open(self.database_file) as file:
            data = json.load(file)
        file.close()
        
        stuff = {
            "username": username,
            "user_data": {
                "balance": 10,
                "plants": [
                    {
                        "nickname": "Name me!",
                        "realname": "Aloe vera",
                        "sciname": "Aloe vera",
                        "birthday": 1698890452.0,
                        "water": 84,
                        "water_decay_rate": 2,
                        "last_water": 1700098006.4412186,
                        "food": 46.0,
                        "food_decay_rate": 1,
                        "last_feed": 1700097960.1149216,
                        "xp": "65",
                        "money_rate": 10
                    }
                ]
            }
        }
        
        data['users'].append(stuff)
        
        with open('database/database.json', 'w') as f:
            json.dump(data, f)
        f.close()