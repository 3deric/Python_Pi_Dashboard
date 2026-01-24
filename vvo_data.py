import requests
import pprint
import datetime
from datetime import timezone
import re
import pytz

def get_vvo_data():
    url = 'https://webapi.vvo-online.de/dm'
    attributes = {
    "stopid": "33000028",
    "limit": 10,
    "mot": [
        "Tram",
        "CityBus",
        "IntercityBus",
        "SuburbanRailway",
        "Train",
        "Cableway",
        "Ferry",
        "HailedSharedTaxi"
        ]
    }
    response = requests.post(url, json = attributes)
    result_dict = response.json()
    return result_dict

def get_data_entry(data : dict, i : int,  key : str) -> str:
    try:
        return data['Departures'][i][key]
    except:
        return 'No Data'

def get_data_time(data: str) -> datetime.time:
    try:
        return datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    except:
        return datetime.datetime.now()


def convert_dotnet_date(dotnet_date_str):
    match = re.search(r'/Date\((\d+)([+-]\d{4})\)/', dotnet_date_str)
    if not match:
        raise ValueError("Invalid .NET date format")
    timestamp_ms = int(match.group(1))
    offset_str = match.group(2)
    timestamp_seconds = timestamp_ms / 1000.0
    utc_datetime = datetime.datetime.fromtimestamp(timestamp_seconds, tz=datetime.timezone.utc)
    offset_hours = int(offset_str[1:3])
    offset_minutes = int(offset_str[3:5])
    if offset_str[0] == '-':
        offset_hours = -offset_hours
        offset_minutes = -offset_minutes

    offset_minutes_total = offset_hours * 60 + offset_minutes
    local_datetime = utc_datetime + datetime.timedelta(minutes=offset_minutes_total)
    tz = pytz.timezone('Europe/Berlin')
    local_datetime = local_datetime.now(tz)
    return local_datetime

if __name__ == "__main__":
    time = '/Date(1769273754966+0100)/'
    result = convert_dotnet_date(time)
    print(f"Result: {result}")
    print(f"Formatted: {result.strftime('%Y-%m-%d %H:%M:%S')}")

# data = get_vvo_data()
    # #pprint.pprint(data)
    # for dep in data['Departures']:
    #     dep_id = ''
    #     dep_line = ''
    #     dep_dir = ''
    #     dep_time_sched = ''
    #     dep_time_real = ''
    #
    #     try:
    #         dep_id = dep['Id']
    #     except:
    #         print("No ID found")
    #     try:
    #         dep_line = dep['LineName']
    #     except:
    #         print("No Line found")
    #     try:
    #         dep_dir = dep['Direction']
    #     except:
    #         print("No Direction found")
    #     try:
    #         dep_time_sched = dep['ScheduledTime']
    #     except:
    #         print("No Scheduled Time found")
    #     try:
    #         dep_time_real = dep['RealTime']
    #     except:
    #         print("No Real Time found")
    #     try:
    #         dep_state = dep['State']
    #     except:
    #         print("No State found")
    #
    #     print(dep_line)
    #     print(dep_dir)
    #     print(dep_time_sched)
    #     print(dep_time_real)
    #     print(dep_state)
    #print(get_vvo_data())