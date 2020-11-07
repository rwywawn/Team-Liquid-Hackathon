from flask import Flask, request
import requests
from config import Config

app = Flask(__name__)

@app.route('/')
def index():

    print(request)
    print(request.args)
    #code = request.args['code']
    #headers = {"Authorization": (Config['token'])}
    #payload = {
        #"client_id": Config['client_id'],
        #"client_secret": Config['client_secret'],
        #"grant_type": "authorization_code",
        #"code": code,
        #"redirect_uri": 
    #}

    #userJSON = requests.post(f"https://discord.com/api/oauth2/token{code}", headers=headers, data=)
    #print ("hello")
    #print (userJSON)
    #print (userJSON.reason)
    #print(userJSON.text.encode('utf8'))
    return
    # return userJSON.text  # send text to web browser

@app.route("/auth", methods = ["get"])
def auth():
    return request.args['code']

if __name__ == '__main__':
    app.run(port=80, debug=True)