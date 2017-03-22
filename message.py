import os
from twilio import twiml
from twilio.rest import TwilioRestClient
import uuid
import threading
import requests
from response_builder import build_sent_notif
from redis_store import save_message, delete_message

twilio_client = TwilioRestClient()
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)



def send_sms(phone, message):
    twilio_client.messages.create(to=phone, from_=TWILIO_NUMBER,
                                  body=message)

class Message:
    def __init__(self, to_number, text, min_delay, response_url):
        self.to_number = to_number
        self.text = text
        self.id = int(uuid.uuid4())
        self.min_delay = min_delay
        self.response_url = response_url


    def start_timer(self):
        timer = threading.Timer(self.min_delay*60, self.send)
        timer.start()
        save_message(self)
        return timer

    def cancel(self):
        self.timer.cancel()
        delete_message(self)

    def send(self):
        send_sms(self.to_number, self.text)
        r = requests.post(self.response_url, data=build_sent_notif())
        delete_message(self)
