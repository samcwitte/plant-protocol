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

    # return client id
    # only getter with input username (the initial get function that returns client id)
    def getClientId(self, username):
        # load in the database
        with open(self.database_file, 'r') as file:
            data = json.load(file)

        for user in data['users']:
            if user['username'] == username:
                return user['client_id']

        return None

    # return user data... used in other getters
    def getUserData(self, username):
        # load in the database
        with open(self.database_file, 'r') as file:
            data = json.load(file)

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
    