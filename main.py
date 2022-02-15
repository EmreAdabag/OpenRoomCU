from flask import Flask, request, render_template
from datetime import datetime as dt
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import random
from roomsearch import *



app = Flask(__name__)



today = dt.today()
last_search_time= today + datetime.timedelta(days=-1)
populate_schedule(today.date())

scheduler = BackgroundScheduler()
scheduler.add_job(func=populate_schedule, args=[dt.today().date()], trigger="cron", hour=0, minute=0,second=0)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route("/", methods=["GET"])
def search_now():
    global empty_rooms
    global last_search_time

    now = dt.today()
    day_length = datetime.timedelta(hours=now.hour, minutes=now.minute,seconds=now.second).total_seconds()
    now_mins = day_length/60

    if (now-last_search_time).total_seconds() > 300:
        last_search_time=now
        empty_rooms = find_rooms([now_mins,now_mins+30])
        
    return render_template('index.html', room=empty_rooms[random.randint(0,len(empty_rooms) -1)][0])


@app.route("/room-later",methods=["GET","POST"])
def room_later():
    if request.method == 'GET':
        return render_template('session.html',results='')
    
    else:
        print(request.form['start-time'])
        print(type(request.form['start-time']))
        start_time = list(map(int, request.form['start-time'].split(':')))
        end_time = list(map(int, request.form['end-time'].split(':')))
        start_mins = start_time[0]*60+start_time[1]
        end_mins = end_time[0]*60+end_time[1]

        if end_mins < start_mins:
            return render_template('session.html', results='', message="please input a valid time slot")

        res = find_rooms([start_mins, end_mins])
 
        return render_template('session.html', results=res)





if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    




