import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACe200567e6352dfbad1a8c404c3fde1d8'
    TWILIO_SYNC_SERVICE_SID = 'IS7b9f66a0a09d822338a3730504c764b4'
    TWILIO_API_KEY = 'SK3a0c876a56b0f25567ff7744d18bfd7e'
    TWILIO_API_SECRET = 'cbo0oEUkqjiHnz7P48j4XYr3rZ52lora'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
   txt_notpad = request.form['text'] 
   with open('workfile.txt', 'w') as f:
       f.write(txt_notpad)
        
   path = 'workfile.txt'
   return send_file(path, as_attachment = True)


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
