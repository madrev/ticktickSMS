# ticktickSMS

You know that one guy on your Slack team who never responds to messages? **ticktickSMS** is a Slack app that lets you bother him better.

ticktickSMS utilizes the Twilio API to send SMS messages to your recipient's phone number (as retrieved from your Slack team's user directory) on a specified timeout. These messages are cancellable using a button visible both to the sender and receiver.

![from_slack](https://github.com/madrev/ticktickSMS/blob/master/docs/screenshots/from_slack.png)

Replies to SMS from the receiver are forwarded back into the conversation:

![to_slack](https://github.com/madrev/ticktickSMS/blob/master/docs/screenshots/to_slack.png)

ticktickSMS is written in Python 3.6 using the Flask microframework. It is in the process of being converted from a single-team Slack app to a distribution-ready app that any team can use. Meanwhile, if you want to get this project running locally -- and don't mind hunting down your own Slack and Twilio tokens -- check out the [local setup instructions](./docs/local_setup.md).

## Soon to come
* OAuth 2.0 token exchange and permissions (for distribution in Slack app directory)
* Auto-recovery of active messages from Redis store
