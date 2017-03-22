import json

def build_success_response(time, message, timer_id):
    resp = {
        "response_type": "in_channel",
        "text": f"Your message will be sent in {time} minutes.",
        "attachments": [
        {
        "text": message,
        "fallback": "Sorry, we can't display the text here."
        },
        {
        "callback_id": str(timer_id),
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

def build_cancel_response():
    resp = {
    "replace_original": True,
    "text": "Your message has been canceled."
    }
    return json.dumps(resp)

def build_sent_notif():
    resp = {
    "replace_original": True,
    "text": "Your message has been sent."
    }
    return json.dumps(resp)
