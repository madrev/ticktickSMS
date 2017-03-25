from redis_store import save_recipient

def format_phone(phone):
    if phone.find("+") == -1:
        res = "+1"
        for i in range(0, len(phone)):
            char = phone[i]
            if i == 0 and char == "1":
                continue
            elif char.isdigit():
                res += char
            else:
                continue
        return res
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
