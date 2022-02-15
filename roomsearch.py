from rooms_bookings import *

    
def populate_schedule(date):
    global room_schedules
    global room_ids

    room_schedules = request_bookings(date)
    room_ids = request_buildings(date)
    

def find_rooms(period):
    open_rooms = []
    #res = []        

    # for room in room_schedules:
        
    #     room_id = int(room)
    #     room = room_schedules[room]

    #     i = 0
    #     #while i is in range and start time is after the current time
    #     while(i < len(room) and period[0]>room[i]): i+=1

    #     #if start time is after all bookings or start time is even and end time is before the next time
    #     if (i == len(room) or (i%2 == 0 and period[1]<room[i])):
    #         open_rooms.append(room_id)       

    for room in room_ids:
        try:
            room_schedule = room_schedules[room]
        except: 
            open_rooms.append([room_ids[room]['name'],room_ids[room]['capacity'],room])       
            continue
        i = 0

        #while i is in range and start time is after the current time
        while(i < len(room_schedule) and period[0]>room_schedule[i]): i+=1

        #if start time is after all bookings or start time is even and end time is before the next time
        if (i == len(room_schedule) or (i%2 == 0 and period[1]<room_schedule[i])):
            open_rooms.append([room_ids[room]['name'],room_ids[room]['capacity'],room])       

    #for room in open_rooms:
    #    res.append([room_ids[room]['name'],room_ids[room]['capacity'],room])    

    open_rooms.sort(reverse=False, key=lambda a: a[1])
    result = filter(lambda a: room_ids[a[2]]['capacity'] > 0, open_rooms)

    return(list(result))


if __name__=='__main__':
    from datetime import datetime as dt
    populate_schedule(dt.today().date())
    find_rooms([15 * 60 + 30, 16 * 60 + 30])