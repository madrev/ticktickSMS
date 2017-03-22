import redis
import pickle


db = redis.StrictRedis(host='localhost', port=6379, db=0)

def save_message(message):
    pickled_message = pickle.dumps(message)
    db.hset("messages", message.id, pickled_message)

def retrieve_message(id):
    return pickle.loads(db.hget("messages", id))

def delete_message(id):
    return db.hdel("messages", id)
