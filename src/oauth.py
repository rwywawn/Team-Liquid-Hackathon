import requests
class Oauth(object):
    client_id ="774475024059990057"
    client_secret="mnM2JSWhPz6D73TyuSM2dniiRyuUxdjB"
    scope="connections"
    redirect_uri="http://127.0.0.1:5000/auth"
    discord_login_url="https://discord.com/api/oauth2/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}".format(client_id,redirect_uri,scope)
    discord_token_url="https://discord.com/api/oauth2/token"
    discord_api_url="https://discordapp.com/api"


    @staticmethod
    def getAccessToken(code):
           payload={
               'client_id':Oauth.client_id,
               'client_secret':Oauth.client_secret,
               'grant_type':"authorization_code",
               'code':code,
               'redirect_uri':Oauth.redirect_uri,
               'scope':Oauth.scope
           } 
           headers ={
               'Content-Type':'application/x-www-form-urlencoded'
           }

           accessToken=requests.post(url=Oauth.discord_token_url,data=payload,headers=headers)
           token=accessToken.json()
           print (token,"SADf")
           return token["access_token"]

    def getUserData(accessToken):
        url=Oauth.discord_api_url+"/users/@me/connections"

        headers={
            'Authorization':"Bearer {}".format(accessToken)
        }
        userData=requests.get(url=url,headers = headers)
        return userData.json()