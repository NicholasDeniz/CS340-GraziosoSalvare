# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 
import os # Reads connection settings from enviornment
from pymongo.errors import PyMongoError # Handles MongoDB errors

# Fields used by the table, sorting, chart, and map
Display_Fields = [
    "animal_id", # Identify animal
    "name", # Display and sort by the name of animal
    "animal_type", # Shows if it is a dog, cat, or other
    "breed", # Display, sort, and chart the breed
    "sex_upon_outcome", # Shows value used by rescue filters
    "age_upon_outcome_in_weeks", # Display and sort by age
    "location_lat", # Latitude for map
    "location_long", # Longitude for map
]

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

        # Uses original settings unless a enviornment setting replaces it
        HOST = os.environ.get('Grazioso_Host', 'localhost')
        PORT = int(os.environ.get('Grazioso_Port', '27017'))
        DB = os.environ.get('Grazioso_Database', 'aac') 
        COL = 'animals' 
        Auth_DB = os.environ.get('Grazioso_Auth', 'admin') # Database where MongoDb account was created
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient(
            host = HOST,
            port = PORT,
            username = USER,
            password = PASS,
            authSource = Auth_DB,
            serverSelectionTimeoutMS = 5000, # Wait 5 seconds from the server
        )
        self.database = self.client[DB] 
        self.collection = self.database[COL] 

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

    def validate_filter(self, data):
        # Accept same dictionary format
        if not isinstance(data, dict):
            raise ValueError("Must be a dictionary")

        # Test fields can be searched together or singularly
        text_fields = [
            "animal_id",
            "name",
            "animal_type",
            "breed",
            "sex_upon_outcome",
        ]

        # Check every field and their value
        for field, value in data.items():
            if field in text_fields:
                if isinstance(value, str):
                    choices = [value] # Single exact text match

                elif isinstance(value, dict) and len(value) == 1 and "$in" in value:
                    # $in accepts a variety of possible matches
                    choices = value["$in"]

                    if not isinstance(choices, list) or not choices:
                        raise ValueError("A $in search needs a something in the list")

                else:
                    raise ValueError("A text search must have text or an $in list")

                # Every requested text value must have text
                for choice in choices:
                    if not isinstance(choice, str) or not choice.strip():
                        raise ValueError("Each search chopice has to have text")

            elif field == "age_upon_outcome_in_weeks":
                # Keeps min/max format
                if not isinstance(value, dict) or not value:
                    raise ValueError("Age needs a $gte min and a $lte max")

                for operator, age in value.items():
                    # $gte means greater than of equal to 
                    # $lte means less than or equal to
                    if operator not in ["$gte", "$lte"]:
                        raise ValueError("Age searches only support $gte and $lte")

                    # Use whole weeks for search limits
                    if type(age) is not int or age < 0:
                        raise ValueError("Enter age limits as whole weeks, zero, or higher")

                # Min can't be larger than max
                if "$gte" in value and "$lte" in value:
                    if value["$gte"] > value["$lte"]:
                        raise ValueError("Min age can't be larger than max age")

            else:
                # Reject invalid fields
                raise ValueError("That search field is not valid")

    def read_page(self, data, page = 1, page_size = 10, fields = None):
        # Check search before passing it to MongoDB
        self.validate_filter(data)

        # Page starts at 1
        # Using type() rejects true or false as page numbers
        if type(page) is not int or page < 1:
            raise ValueError("Page must be a whole numbers starting at 1")

        # Limit a request to between 1 and 100 animals
        if type(page_size) is not int or not 1 <= page_size <= 100:
            raise ValueError("Page size must be a whole number from 1 to 100")

        # Use dashboard fields unless a smaller list is called
        if fields is None:
            fields = Display_Fields

        if not isinstance(fields, list) or not fields:
            raise ValueError("Choose a not empty list of fields")

        # A projection tells MongoDB the fields to return
        # Dash doesn't need MongoDB's ObjectId
        projection = {"_id": 0}

        for field in fields:
            if field not in Display_Fields:
                raise ValueError("The return field is not valid")

            projection[field] = 1 # Include that field in return

        # As an example, page 2 with 10 animals per page skips the first ten
        skip_records = (page - 1) * page_size

        try:
            # Counts all matches without loading all records
            total = self.collection.count_documents(data, maxTimeMS = 5000)

            # Starts with original find operation and uses selected fields
            info = self.collection.find(data, projection)

            # Keeps the database pages in an order
            info = info.sort("_id", 1)

            # Move over the records that belonged to earlier pages
            info = info.skip(skip_records)

            # Requests only the animals needed for the page
            info = info.limit(page_size)

            # Stops a query that is longer than 5 seconds
            info = info.max_time_ms(5000)

            # Converts the smaller result into Python list
            records = list(info)

        except (PyMongoError, OverflowError):
            # Shows a message without sensitive info
            raise RuntimeError("Can't read animals. Check the connection and search values") from None

        # return this page and number of matching animals
        return {
            "records": records,
            "total": total,
        }
        

                                  