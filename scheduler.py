import ticktick
import sched, time
import threading

s = sched.scheduler(time.time, time.sleep)

def schedule_message(sec, phone, message):
    event = s.enter(sec, 1, ticktick.send_sms, (phone, message))
    run_scheduler(s)
    return event

def run_scheduler(s):
    if len(s.queue) == 1:
        threading.Thread(target=s.run).start()
