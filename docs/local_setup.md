# ticktickSMS: Local setup

The ticktickSMS project is currently in development and, when it's ready, will be available in the Slack app directory. Until then, you'll need a number of things to get it running locally...

### Requirements
* Python 3.6
* A [Slack](https://www.slack.com) team to which you have API access
* A Slack app set up at [api.slack.com](https://api.slack.com/apps)
* A [Twilio](https://www.twilio.com) account with one Twilio number set up for SMS
* A [Redis](https://redis.io/) store running locally on port 6379 (or any other that you like; you'll just need to tweak the setup code)
* [ngrok](https://ngrok.com/) to tunnel traffic from Slack and Twilio to your local server
* This repository, cloned or downloaded as a .zip

### Setup instructions

Navigate to ticktickSMS's location on your local machine. Open up a virtualenv to isolate this project from other Python dependencies you may have:

```
virtualenv ticktick
```

```
source ticktick/bin/activate
```

#### Set your environment variables

Here's the tedious part. ticktickSMS needs a bunch of information from Slack and Twilio to work. Run the following at the command line, substituting your credentials. If you need help finding them, check out [this great blog post from Twilio](https://www.twilio.com/blog/2016/05/build-sms-slack-bot-python.html).
```
echo "export TWILIO_ACCOUNT_SID=xxxxxx" >> ~/.bashrc
```
```
echo "export TWILIO_AUTH_TOKEN=xxxxxx" >> ~/.bashrc
```
```
echo "export TWILIO_NUMBER=xxxxxx" >> ~/.bashrc
```
```
echo "export SLACK_WEBHOOK_SECRET=xxxxxx" >> ~/.bashrc
```
```
echo "export SLACK_TOKEN=xxxxxx" >> ~/.bashrc
```

#### Set up ngrok

Make sure you have [ngrok](https://ngrok.com/) downloaded, then get it running:
```
./ngrok http 5000
```
Grab the HTTPS forwarding URL displayed in the terminal, and put it in three places:
* Under 'Messaging/A message comes in' in your Twilio number's configuration area (with /twilio appended)
* Under 'Slash commands' (with a slash command of your choice) in the Slack app management console (with /slack appended)
* Under 'Interactive messages', also in the Slack console (with /slack/button appended)

#### Run it!

Whew, you made it through. Make sure Redis is running locally and run:
```
python ticktick.py
```

If you did all this and it's not working, raise an issue and let me know!
