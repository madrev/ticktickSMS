import os
import scheduler
import json
import pprint
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml
from twilio.rest import TwilioRestClient



app = Flask(__name__)
twilio_client = TwilioRestClient()
slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_INCOMING_TOKEN', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)



def get_recipient_id(channel_id):
    im_call = slack_client.api_call("im.list")
    if im_call.get('ok'):
        for im in im_call['ims']:
            if im['id'] == channel_id:
                return im['user']
    return None

def get_user_phone(user_id):
    user_call = slack_client.api_call("users.info", user=user_id)
    if user_call.get('ok') and 'phone' in user_call['user']['profile']:
        return user_call['user']['profile']['phone']
    return None

def send_sms(phone, message):
    twilio_client.messages.create(to=phone, from_=TWILIO_NUMBER,
                                  body=message)

def build_success_response(time, message):
    resp = {
        "response_type": "in_channel",
        "text": f"Your message will be sent in {time} minutes.",
        "attachments": [
        {
        "text": message
        },
        {
        "callback_id": "cancel",
        "fallback": "Sorry, your browser doesn't support canceling this action.",
        "actions": [
            {
            "name":"cancel",
            "text":"Cancel this SMS",
            "style":"danger",
            "type":"button"
            }
        ]
            }
        ]
    }
    return json.dumps(resp)

def build_failure_response():
    resp = {
    "response_type": "ephemeral",
    "text": "Sorry, your recipient does not have a phone number listed."
    }
    return json.dumps(resp)

@app.route('/twilio', methods=['POST'])
def twilio_post():
    response = twiml.Response()
    message = request.form['Body']
    slack_client.api_call("chat.postMessage", channel="#ticktick",
                          text=message, username='ticktick',
                          icon_emoji=':robot_face:')
    return Response(response.toxml(), mimetype="text/xml"), 200

@app.route('/slack', methods=['POST'])
def slack_post():
    if request.form['token'] == SLACK_WEBHOOK_SECRET:

        pprint.pprint(request.form)
        channel_id = request.form['channel_id']
        recipient_phone = get_user_phone(get_recipient_id(channel_id))
        username = request.form['user_name']
        text = request.form['text']
        response_message = username + " says: " + text

        if recipient_phone != None:
            timer = scheduler.schedule_message(1, recipient_phone, response_message)
            response_text = build_success_response(1, text)
            print(timer)
        else:
            response_text = build_failure_response()
    return Response(response_text, mimetype="application/json"), 200

@app.route('/slack/button', methods=['POST'])
def handle_button():
    pprint.pprint(request.form)
    return Response(), 200



if __name__ == '__main__':
    app.run(debug=True)
