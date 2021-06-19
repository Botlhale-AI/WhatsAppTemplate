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
account_sid = 'AC15d4bb054a6eccb972cde20cb9e1b1da'
auth_token  = '788a0547a47b8dc1121cd184d3036f33'
client      = Client(account_sid, auth_token)

# botlhale 
RereshToken = 'eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.D2FqCm36rDXWD-mWS8OPS83vCo7v7hMxviLs-L_v2FFVTPj2uUVW4pZheH2nn7sgt6lc-Fw-6J5WWUNuqsBQzhSc12Eag_6G9hb_C2YVwxss96wJYMjyZjzvrpY5wkShV9D4wro3JkPeUosQKaiL8OXLQEW_E_6nShDz3Qg7c78DBgaQHEo4t3sYFahbzEulqENdaccvKZGtAZU3LJQ7PhKWBSVY52PJCBw3ygxTzfyCKqkuzyx_-zuM7wCNbg6KRGGQlr7ARn1w0N2vgjg2KyLhO06LoOpmuebaOSgE2sx9G5rLZt0kDHoW6d_TniMxnatwJEqgbW9ne7h3Hro_NQ.D_qpsVb11Aas5Dj5.l_0HxhvWztqiaoV4ze1xp0eakQpbr8SJ2o2rfCDOro48VC3zOr2FF1zyjFyEfZTvm-LGa8R9CsLRQyQUgYQVqyZ9uRi4FP6pVaWDeQw_fqJt72mDk4jDTo24i6fT5b1VbyibHCk7EP8sEOM9ubI8VtxL0X1C0SOfgN09Tson0-fh0AMwCymER2XHyAfqcs9ljtFtZumL4IOc0-K68sbpZQqC4ikS1AG88MANwKSqjiEPUTvbXegC-ahtRDSTpI215ZE3NOJzKk2KdJpIlFOVxKbiHQZtAlwrqounOVUI-indNLb2vDjvrwl6nEyFJ8YpaRZzXOkLLhe_7BtbzI-P8J2RtZYupxaWcCFd_uKVxm6ReH59RoF2PoP7Nj5dUq6anQMCGHBdlR8AF0kohSSKKS59TXtJoxt3J3yb9UifZND2odgUDEAXvU2dcEcAquPNdmaS1uVk24a46JTv5MI0C2bKQ4L9Narcn5_471jAWnOSNZOctPMfsGU-HAVrBC-uTMHsqiTTY5c3lLGKm5yZqTXFTe3N9H8ewbJTZupN4xh3GMrkskI-Y8x3ucZTLUBBwtCjpLUpEh2tiZRADHom2eGKuX2IWdsxJuLu-rTBqGSehfHhr_2AA2hQsWFZB2Vpq8mmfMqp7z8jjy7t7BrHdMHSvuvpSdI_ksn4bfVuJSQg999VO87GBEM2Sm9D1CP0fDdfzamdLfB6v0O34Kgn4RWFh_0iTfPVHLd57-1leAL9aMEnDJDF6Mj3aq5ER9-DWM4Hzp9kPpRFd8ajXWCDH7SxQaCKSK2sArsdWVgcGfWo469Z0sseoRn7QdEo-6JmLENGuTY3zPiu3UbiX9AWwbfZ-ILAlnH_BNj7ebZy8epsyQDYAml4-XATfOuRg2qIon8JyV7Np6IK7PV6BIptqag4sjk4BHC9NBurhoahWQsuRExshYN-suKi-vbyFwEwGbRi5Mdo6-Zlxa8VxQ77sGHekRWTWNWrkkeRS1t9-I5X8363_BiY8bqeppANlRD2UCvNj5nmFPlI48Hq7vdQcxBcKo2HEXfVsa1yG1NcOUK2W-0AAoyvrmSHu_VzqEJYpkRfvmszjIqbY5kPwXoOOcZV_x6S8IdCeWEVt7XbBl99Xf_NF_gkztQ590ur8TY7xh2bh-uXNSR8UiZCfZG6fwFi_4W96WN1OIYaQzIjGwb7YQwKPPjR243S_zEfc0j7S9v4iHOtWXYQD6NWoSlbihMpSR_wUMyPRw6W2ou0HLiK58YjhE-5anTNm9u9G9sTQxMG5MX4eMFV0utnGrd2la4-SwUJOnwKkye8XKTTKCYady6Xj20biAnA9mk.JRasxEDhLwHB2cpv2iHhoQ'
BotID = 'MQWISWIOLTJLVXKS'
LanguageCode = 'English'

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
        ConversationID = users[sender]
        return True
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

    # intitaialise twilio messaging respinse object
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