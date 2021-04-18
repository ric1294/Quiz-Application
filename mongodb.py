from pymongo import MongoClient

DB_NAME = 'Onlinetest'
DB_URL = "mongodb://localhost:27017"
coll = 'User'
databaseserver = MongoClient(DB_URL)
database = databaseserver[DB_NAME]
collection = database[coll]
global user_Data
user_Data = {}

def delete_user():
    x = collection.delete_many({})
    print(x.deleted_count, " documents deleted.")


def ins_data(data, collection):

    Retrieve_data(collection)
    myquery = {'username': data['username']}
    result = collection.count_documents(myquery)

    if result != 0:
        print("Already Exist")
    else:
        print(result)
        success = collection.insert_one(data)
        Retrieve_data(collection)


def Retrieve_data(collection_name):
    for document in collection_name.find():
        print(document)


def register_User():
    print("Register user")

    Retrieve_data(collection)
    choice = input("Press y for register \n Press n for login:")
    if (choice == 'y'):
        username = input("Enter username")
        password = input("Enter password")
        ins_data({'username': username, 'password': password}, collection)
    if choice == 'n':
        Login_user(collection)



def Login_user(collection):
    username = input("Enter username")
    password = input("Enter password")
    myquery = {'username': username}
    result = collection.count_documents(myquery)

    if result != 0:
        print("login in")
    else:
        print("Invalid credentials")
        Retrieve_data(collection)


Retrieve_data(collection)
register_User()
# delete_user()
# insert_Manydata(data, collection)
# highest_salary(collection)
# remove_document(collection)
print("///")
# delete_user()
