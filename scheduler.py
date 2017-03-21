import ticktick
import threading

def schedule_message(min, phone, message):
    timer = threading.Timer(min*60, ticktick.send_sms, (phone, message))
    timer.start()
    return timer

def cancel_message(timer):
    timer.cancel()
