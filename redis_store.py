import redis
import pickle


db = redis.StrictRedis(host='localhost', port=6379, db=0)

def save_message(message):
    pickled_message = pickle.dumps(message)
    db.hset("messages", message.id, pickled_message)

def retrieve_message(id):
    return pickle.loads(db.hget("messages", id))

def delete_message(id):
    db.hdel("messages", id)

def save_recipient(recipient):
    db.hset(recipient.phone, "phone", recipient.phone)
    db.hset(recipient.phone, "username", recipient.username)
    db.hset(recipient.phone, "channel_id", recipient.channel_id)
    db.hset(recipient.phone, "user_id", recipient.user_id)

def get_channel_id(phone):
    return db.hget(phone, "channel_id").decode(encoding="UTF-8")

def get_username(phone):
    return db.hget(phone, "username").decode(encoding="UTF-8")
