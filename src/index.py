from flask import Flask, request, redirect, render_template
import requests
from config import Config
from oauth import Oauth


app = Flask(__name__)

@app.route('/',methods=["get"])
def index():

    print(request)
    print(request.args)
    
    return redirect(Oauth.discord_login_url)

@app.route("/auth", methods = ["get"])
def auth():
    code=request.args.get("code")
    accessToken= Oauth.getAccessToken(code)
    connectionData=Oauth.getConnectionData(accessToken)
    userData=Oauth.getUserData(accessToken)
    connections={}
    connections['user_id']=userData['id']
    connections['email']= userData['email'] if userData['email'] else None

    for i in connectionData:
        if i['type'] =="steam":
            connections['steam_name']=i['name']
            connections['steam_id']=i['id']

    if ("steam" in connections.keys()):
        return app.send_static_file("retry.html")
    response=Oauth.findData("authentication",connections['user_id'])
  
    if not ("Item" in response.keys()):
        print ("here")
        Oauth.inputData("authentication",connections)

    
    return  app.send_static_file("index.html")
if __name__ == '__main__':
    app.run( debug=True) 

