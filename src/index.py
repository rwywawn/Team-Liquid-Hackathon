from flask import Flask, request, redirect
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
    userData=Oauth.getUserData(accessToken)
    connections=""
    arr=[]
    for i in userData:
        connections=connections+i["type"]+" "
        arr.append(i['type'])
    if "steam" in arr:
        redirect('https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fdiscord.com%2Fapi%2Fconnections%2Fsteam%2Fcallback%3Fstate%3D18f58d3a02063b7118c9fcee0caca871&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select')
    return connections

if __name__ == '__main__':
    app.run( debug=True)