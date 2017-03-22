import os
import json

from response_builder import build_success_response, build_failure_response, build_cancel_response
from message import Message
from redis_store import delete_message
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml




app = Flask(__name__)


slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)

timers = {}


def log_timer(message_id, timer):
    timers[message_id] = timer

def parse_command(command):
    words = command.split(" ")
    if words[0].isdigit():
        min_delay = int(words[0])
        del words[0]
        return (min_delay, " ".join(words))
    else:
        return (5, command)


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
        channel_id = request.form['channel_id']
        recipient_id = get_recipient_id(channel_id)
        recipient_phone = get_user_phone(recipient_id)

        if recipient_phone != None:

            response_url = request.form['response_url']
            username = request.form['user_name']
            command = request.form['text']
            parsed = parse_command(command)
            min_delay = parsed[0]
            text = parsed[1]
            response_message = username + " says: " + text
            msg = Message(recipient_phone, text, min_delay, response_url)
            timer = msg.start_timer()
            log_timer(msg.id, timer)
            response_text = build_success_response(min_delay, text, msg.id)

        else:
            response_text = build_failure_response()
    return Response(response_text, mimetype="application/json"), 200

@app.route('/slack/button', methods=['POST'])
def handle_button():
    payload = json.loads(request.form['payload'])
    message_id = payload['callback_id']
    timers[message_id].cancel()
    delete_message(message_id)
    response_text = build_cancel_response()
    return Response(response_text, mimetype="application/json"), 200



if __name__ == '__main__':
    app.run(debug=True)
