import os
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

@app.route('/twilio', methods=['POST'])
def twilio_post():
    response = twiml.Response()
    message = request.form['Body']
    slack_client.api_call("chat.postMessage", channel="#ticktick",
                          text=message, username='ticktick',
                          icon_emoji=':robot_face:', reply_broadcast="true")
    return Response(response.toxml(), mimetype="text/xml"), 200

@app.route('/slack', methods=['POST'])
def slack_post():
    if request.form['token'] == SLACK_WEBHOOK_SECRET:
        print(request.form)
        channel_id = request.form['channel_id']
        recipient_phone = get_user_phone(get_recipient_id(channel_id))
        username = request.form['user_name']
        text = request.form['text']
        response_message = username + " says: " + text
        if recipient_phone != None:
            twilio_client.messages.create(to=recipient_phone, from_=TWILIO_NUMBER,
                                          body=response_message)
        else:
            # TODO: tell the user the message isn't happening
            print("No text sent")
    return Response(), 200


if __name__ == '__main__':
    app.run(debug=True)
