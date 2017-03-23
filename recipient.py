from redis_store import save_recipient

def format_phone(phone):
    if phone.find("+") == -1:
        if phone[0] != "1":
            return "+1" + phone
        else:
            return "+" + phone
    else:
        return phone

class Recipient:
    def __init__(self, phone, username, channel_id, user_id):
        self.phone = format_phone(phone)
        self.channel_id = channel_id
        self.username = username
        self.user_id = user_id

    def save(self):
        save_recipient(self)
