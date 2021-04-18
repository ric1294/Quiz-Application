from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from question import *

app = Flask(__name__)

DB_NAME = 'Onlinetest'
DB_URL = "mongodb://localhost:27017"

coll = ['User', 'History']

databaseserver = MongoClient(DB_URL)
database = databaseserver[DB_NAME]
collection = []
for single_coll in coll:
    collection = database[single_coll]
global user_Data
user_Data = {}
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
SESSION_TYPE = 'redis'
app.config.from_object(__name__)


def delete_user():
    x = collection[0].delete_many({})
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
    print("call get data")
    for document in collection_name.find():
        print(document)
    print(list(collection_name.find()))
    # return collection_name.find()


@app.route('/')
def index():
    print(session.get("username"))
    return render_template("index.html")


@app.route('/highest/<string:subject>', methods=['GET', 'POST'])
def highest(subject):
    print(subject,collection[1].distinct('username'), "...............result")

    result = list(collection[1].find({'subject': subject}))
    print(result)
    return render_template("highest.html", score=result)


@app.route('/quiz/result/<string:subject>', methods=['GET', 'POST'])
def result(subject):
    print(subject, "...............result")
    score = 0
    questions = 0
    if request.method == 'POST':
        req = request.form
        print(req, answers[subject])
        if len(req)==0:
            collection[1].insert_one({'username': session.get("username"), 'subject': subject, 'score': 0})
            return render_template("result.html", subject=subject, score=score,
                                   percentage=0,questions=len(answers[subject].items()))
        else:
            for actual, expected in zip(req.items(), answers[subject].items()):
                questions = questions + 1
                if actual == expected:
                    score = score + 1
            print(session.get("username"))
            print("total question",questions,"###############",score,"score")
            finalper = (score / len(answers[subject].items()) * 100)
            collection[1].insert_one({'username': session.get("username"), 'subject': subject, 'score': score})
            return render_template("result.html", subject=subject, score=score, questions=questions,
                           percentage=finalper)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/quiz/<string:subject>', methods=['GET', 'POST'])
def quiz(subject):
    print(questions[subject], "Quiz fxn")
    return render_template("quiz.html", questions=questions[subject], subject=subject)


@app.route('/subjects')
def subjects():
    document = Retrieve_data(collection)
    print(document, "value")
    return render_template("user.html", document=document)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("...")
    emailerror = ""
    passerror = ""
    if request.method == 'POST':
        print("post")
        if len(request.form['user']) != 0 and len(request.form['pass']) != 0:
            myquery = {'username': request.form['user'], 'password': request.form['pass']}
            print(myquery)
            Retrieve_data(collection[0])
            result = collection[0].count_documents(myquery)

            if result != 0:
                print("login in")
                session['username'] = request.form['user']
                return redirect(url_for('subjects'))

            else:
                print("Invalid credentials")
                return render_template("login.html", existnotaccount="Invalid Username or Password")
        if request.form['user'] == '':
            emailerror = "Email is required"
        if request.form['pass'] == '':
            passerror = "Password is required"
    print("..1.")
    return render_template("login.html", emailerror=emailerror, passerror=passerror)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("...")
    emailerror = ""
    passerror = ""
    if request.method == 'POST':
        print("post")
        if len(request.form['user']) != 0 and len(request.form['pass']) != 0:
            myquery = {'username': request.form['user']}
            result = collection[0].count_documents(myquery)

            if result != 0:
                print("Already Exist")
                return render_template("signup.html", existaccount="Username is taken")
            else:
                print("Insert")
                print(result)
                success = collection[0].insert_one({'username': request.form['user'], 'password': request.form['pass']})
                Retrieve_data(collection[0])
                return render_template("login.html", accountcreated="Congratulations! Your account has been created")
        if request.form['user'] == '':
            emailerror = "Email is required"
        if request.form['pass'] == '':
            passerror = "Password is required"
    print("..1.")
    return render_template("signup.html", emailerror=emailerror, passerror=passerror)


if __name__ == '__main__':
    app.run(debug=True)
