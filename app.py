from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from flask import Flask, request, render_template
import requests
import json
import os

app = Flask(__name__)

# local non-persistent database
# use an actual database for persistency, but this will work too
users = {}

# twillio
account_sid = '<account_sid>'
auth_token  = '<auth_token>'
client      = Client(account_sid, auth_token)

# botlhale 
RereshToken = '<RereshToken>'
BotID = '<BotID>'
LanguageCode = '<LanguageCode>'

def generateIdToken():
    url = "https://dev-botlhale.io/generateAuthToken"

    payload={'REFRESH_TOKEN': RereshToken}
 
    response = requests.request("POST", url, data=payload)
    try:
        return response.json()["AuthenticationResult"]["IdToken"]
    except:
        return None

IdToken = generateIdToken()      

def startConversation(BotID, LanguageCode):
    url = "https://dev-botlhale.io/startConversation"

    payload={
        'BotID': BotID,
        'LanguageCode': LanguageCode
    }
    headers = {"Authorization": IdToken}

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        return response.json()["ConversationID"]
    except:
        return None

def conversationStarted(sender):
    try:
        return users[sender] != None
    except:
        return False
        
def sendMessage(message, ConversationID):
    url = "https://dev-botlhale.io/message"

    payload={
        'BotID': BotID,
        'LanguageCode': LanguageCode,
        'ConversationID': ConversationID,
        'MessageType': 'text',
        'ResponseType': 'text',
        'TextMsg': message
    }
    
    headers = {"Authorization": IdToken}

    response = requests.request("POST", url, headers=headers, data=payload)
    # try:
    response = response.json()
    print(response)

    # intitaialise twilio messaging response object
    TwilioMessagingResponse = MessagingResponse()

    # restructure response object for twilio and WhatsApp
    TextResponse = response['TextResponse']
    Buttons = response['Buttons']

    for response in TextResponse:
        print(response)
        TwilioMessagingResponse.message(response)
    
    for response in Buttons:
        print(response)
        response = '- ' + response['title']
        TwilioMessagingResponse.message(response)

    return TwilioMessagingResponse
    # except:
    #     return None


@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        # get sender and message from twilio webhook
        sender = request.form.get("From", '')
        message = request.form.get("Body", '').lower()

        # check if sender has started a conversation
        if not conversationStarted(sender):
            users[sender] = startConversation(BotID, LanguageCode)

        ConversationID = users[sender]

        # send message to bot and get bot responses
        TwilioMessagingResponse = sendMessage(message, ConversationID)

        return str(TwilioMessagingResponse)

    return 'connecting to twilio'


if __name__ == "__main__":
    app.run()
