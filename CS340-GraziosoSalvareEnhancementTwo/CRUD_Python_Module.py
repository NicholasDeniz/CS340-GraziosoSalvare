# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = username
        PASS = password
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: #Check that data was passed in the method
            self.database.animals.insert_one(data)  # data should be dictionary #Insert the data into the animals collection
            return True #Return True if worked
        else: 
            return False #Return False if there was no data
            #raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, data):
        if data is not None: #Check if a search was passed in the method
            info = self.database.animals.find(data) #Find what matches
            return list(info) #Put into list
        else:
            return [] #return empty list
        
    #Create method to implement the U in CRUD
    def update(self, data, dataUpdate):
        if data is not None and dataUpdate is not None: #Makes sure that the arguments were in
            info = self.database.animals.update_many(data, dataUpdate) #Update the object that matches
            return info.modified_count #Return the number of objectsts changed in collection
        else:
            return 0 #Just return 0 if something wasn't there
        
    #Create method to implement the D in CRUD
    def delete(self, data):
        if data is not None: #Check if search went hrough
            info = self.database.animals.delete_many(data) #Delete if it matches
            return info.deleted_count #Return deleted objects number
        else:
            return 0 #Return 0 if nothing went in
            