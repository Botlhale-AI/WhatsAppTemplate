# WhatsAppTemplate

<!-- ![WhatsAppTemplate](fbdeploy.jpeg) -->

## Create a Twilio Project
The WhatsApp Template connects your bot to WhatsApp, using [Twilio](www.twilio.com/referral/w9PylM). To use Twilio, the first thing you need to do is create a twilio account and a twilio project. Each Twilio account has an `account_sid` and `auth_token`. You need to keep these safe, you will use them later.

## Runninng the template
Inside this repo, there is Flask application on `app.py`. Flask is a Python framework, so to run the app you'll need to install the framework, as well as the Twilio library using `pip install flask twilio`. Inside `app.py` you need to set the `account_sid` and `auth_token` for Twilio. You also need to set `RefreshToken`, `BotID` and `LanguageCode` for the bot you'll be using. The `RefreshToken` can be found on the NLT platform, under Profile -> API -> Refresh token; the `BotID` can be found under Deploy -> Bot ID; and the `LanguageCode` is simple the language of your bot, capitilised (English, IsiZulu, etc)

You can then run the app using `python app.py` - this will spin up a development server on `http://localhost:5000`. If you want to run the app on a remote production server such as on DigitalOcean/GCP/AWS, you can following the instructions on how to deploy the flask app [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04). 

If you're running the app on localhost, you will need an extra step to make your app publicly available on the internet. To do this you need to expose localhost over a secure tunnel, using ngrok/localtunnel/serveo/teleconsole/pagekite. To use ngrok, download it from [here](https://ngrok.com/download) and run the ngrok file on your terminal using `./ngrok http 5000`. The app will now be exposed on an ngrok url. At this point, you should be running both the flask app and ngrok on separate terminals/CMDs.

## Setting up the twilio webhook
Finally, you need to add the ngrok endpoint to Twilio's WhatsApp webhook. To do:
- Log into your Twilio account; logging in will take to your project dashboard
- From the dashboard, go to Messaging -> Try it out -> send a WhatsApp message; this will take you to Twilio's sandbox environment for WhatsApp
- Copy the `WhatsApp number` and `join` code, you will need these later
- Skip the `Learn: Twilio Sandbox for WhatsApp` instructions until you get to the step: `Configure your Sandbox`
- Copy and paste your secured ngrok url onto the webook that says `WHEN A MESSAGE COMES IN` and click `save`
- Make sure to copy the https not http url
- Make sure that the http method on the webhook is set `HTTP Post`
- You can leave the `STATUS CALLBACK URL` webhook empty

## Start chatting on WhatsApp
You can chat to your bot by sending a messsage to the `WhatsApp number` provided by twilio. To connect to twilio for the first time, you need to send the `join` code `(join xxxxxxx-yyyyyy)`; finally, you can start chatting with your bot.
