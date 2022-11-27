# https://www.w3schools.com/python/python_mongodb_getstarted.asp
import pymongo
# practice using 
myclient = pymongo.MongoClient("mongodb+srv://KevinLi:Kevinpower1@ourcluster.eemanbw.mongodb.net/?retryWrites=true&w=majority")

mydb = myclient["mydatabase"]

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")

mycol = mydb["customers"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)

mydict = { "name": "Peter", "address": "Lowstreet 27" }

x = mycol.insert_one(mydict)

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

x = mycol.insert_many(mylist)

print(x.inserted_ids)
