import os
from flask import Flask, render_template, request, redirect, url_for, jsonify 
import json
from waitress import serve
# import shutil

def createFile():
    if not os.path.exists('user_data.json'):
        user_intdata=[]
        data = {
            "name": "Mohamed Abdelrahman",
            "phone": "+966-587858758",
            "email": "test@test.com",
            "age": "35"
        }
        user_intdata.append(data)
        with open('user_data.json', 'w') as json_file:
                json.dump(user_intdata, json_file, indent=4)

app = Flask(__name__)

# Initialize an empty list to store user data
user_data = []

# Function to check if an email is unique
def check_phone_exists(json_file, value):
    with open(json_file, 'r') as json_data:
        data = json.load(json_data)
        for index in data:
            # print (value)
            if index['phone']==value:
                return True
        return False

def check_email_exists(json_file, value):
    with open(json_file, 'r') as json_data:
        data = json.load(json_data)
        for index in data:
            # print (value)
            if index['email']==value:
                return True
        return False
    
@app.route('/')
def registration_form():
    # backup file before start
    # createFile()
    # shutil.copyfile('user_data.json', 'user_data_bk.json')
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    createFile()
    name = request.form['name']
    phone = request.form['phone']
    phone = phone.replace(' ', '').replace('+966', '').replace(' ','').replace('^05', '')
    phone = '+966-5'+phone
    email = request.form['email'].replace(' ', '')
    email = email.lower()
    age = request.form['age']

    check_email_exists_bool = check_email_exists('user_data.json', email)
    check_phone_exists_bool=check_phone_exists('user_data.json', phone)

    # Basic email validation
    if check_email_exists_bool or check_phone_exists_bool:
        return "Email is already registerd!"
    else:
        # Store the user data in a dictionary
        user = {
            'name': name,
            'phone': phone,
            'email': email,
            'age': age
        }
        user_data.append(user)

        # Store the user data in a JSON file
        with open('user_data.json', 'a') as json_file:
            json.dump(user_data, json_file, indent=4)

        # Convert file to correct json format
        fin = open("user_data.json", "rt")
        fout = open("user_data_final.json", "wt")
        for line in fin:
            fout.write(line.replace('][', ','))
        fin.close()
        fout.close()
        os.remove('user_data.json')
        os.rename('user_data_final.json', 'user_data.json')

        return "Registration successful!"

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=9080)

# flask.exe --app  .\StarterApp.py  run --host=0.0.0.0 --port=9080
# pyinstaller --icon=registration.ico  --add-data "templates;templates" -w -F .\app.py --onefile
