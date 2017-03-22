import os
# import scheduler
import json
import redis
from response_builder import build_success_response, build_failure_response, build_cancel_response
from message import Message
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml




app = Flask(__name__)
db = redis.StrictRedis(host='localhost', port=6379, db=0)


slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)

# timers = {
# "counter": 0
# }

#
# def log_timer(timer):
#     timers[timers["counter"]] = timer
#     timers["counter"] += 1
#

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
        print(request.form)
        channel_id = request.form['channel_id']
        recipient_id = get_recipient_id(channel_id)
        recipient_phone = get_user_phone(recipient_id)

        if recipient_phone != None:
            # timer = scheduler.schedule_message(1, recipient_phone, response_message)
            # log_timer(timer)
            # print(timers)
            # timer_id = timers["counter"] - 1
            response_url = request.form['response_url']
            username = request.form['user_name']
            text = request.form['text']
            response_message = username + " says: " + text
            msg = Message(recipient_phone, text, 1, response_url)
            msg.start_timer()
            response_text = build_success_response(1, text, msg.id)

        else:
            response_text = build_failure_response()
    return Response(response_text, mimetype="application/json"), 200

@app.route('/slack/button', methods=['POST'])
def handle_button():
    payload = json.loads(request.form['payload'])
    timer_id = int(payload['callback_id'])
    timer = timers[timer_id]
    scheduler.cancel_message(timer)
    response_text = build_cancel_response()
    return Response(response_text, mimetype="application/json"), 200



if __name__ == '__main__':
    app.run(debug=True)
