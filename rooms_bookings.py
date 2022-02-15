import requests
import json
import datetime

booking_url = 'https://ems.cuit.columbia.edu/EmsWebApp/ServerApi.aspx/GetBrowseLocationsBookings'

building_info_url = 'https://ems.cuit.columbia.edu/EmsWebApp/ServerApi.aspx/GetBrowseLocationsRooms'

booking_headers = {
'authority': 'ems.cuit.columbia.edu',
'method': 'POST',
'path': '/EmsWebApp/ServerApi.aspx/GetBrowseLocationsBookings',
'scheme': 'https',
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'content-length': '356',
'content-type': 'application/json; charset=UTF-8',
'dea-csrftoken': '81df8ba5-f520-46f5-b84f-ca8cd0898882',
'origin': 'https://ems.cuit.columbia.edu',
'referer': 'https://ems.cuit.columbia.edu/EmsWebApp/BrowseForSpace.aspx',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"macOS"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}

building_info_headers = {
'authority': 'ems.cuit.columbia.edu',
'method': 'POST',
'path': '/EmsWebApp/ServerApi.aspx/GetBrowseLocationsRooms',
'scheme': 'https',
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'content-length': '356',
'content-type': 'application/json; charset=UTF-8',
'origin': 'https://ems.cuit.columbia.edu',
'referer': 'https://ems.cuit.columbia.edu/EmsWebApp/BrowseForSpace.aspx',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'x-requested-with': 'XMLHttpRequest',
}


def payload(date):
        tomorrow = date+datetime.timedelta(days = 1)
        return '{"filterData":{"filters":[{"filterName":"StartDate","value":"'+ str(date) +' 12:00:00","displayValue":null,"filterType":3},{"filterName":"EndDate","value":"'+ str(tomorrow) +' 12:00:00","filterType":3,"displayValue":""},{"filterName":"Locations","value":"-1","displayValue":"(all)","filterType":8},{"filterName":"TimeZone","value":"61","displayValue":"","filterType":2}]}}'


def request_bookings(date):
    r = requests.post(booking_url, headers = booking_headers, data = payload(date))
    events = json.loads\
            (json.loads(r.text)["d"])\
            ["Bookings"]
    
    rooms = {}
    
    for event in events:
        roomID = event["BookingInRoomId"]
        if (roomID not in rooms):
            rooms[roomID] = []

        start = event['StartPosition']
        end = start + event['EventWidth'] + event['TeardownWidth']
        rooms[roomID].append(start)
        rooms[roomID].append(end)

    for room in rooms:
        rooms[room] = sorted(rooms[room])
        
    return rooms


def request_buildings(date):
    b = requests.post(building_info_url, headers = building_info_headers, data = payload(date))
    building_dict = json.loads\
        (json.loads(b.text)\
        ['d'])
    
    room_ids = {}

    for building in building_dict['Buildings']:
        for building_room in building['Rooms']:
            room_ids[building_room['Id']] = {'name':building_room['DisplayText'], 'capacity':int(building_room['Capacity'])}

    return room_ids

