import requests
from datetime import datetime, timezone, timedelta
import re
import pytz

class VVO():
    def __init__(self):
        self.timezone = pytz.timezone('Europe/Berlin')
        self.data = {}

    def retrieve_stop_data(self, stopid : str):
        url = 'https://webapi.vvo-online.de/dm'
        attributes = {
        "stopid": stopid,
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
        result = response.json()
        self.data = result

    def get_data_value(self, i : int,  key : str) -> str:
        try:
            return self.data['Departures'][i][key]
        except:
            return 'N/A'

    def get_data_entry(self, i: int) -> tuple():
        try:
            line = self.data['Departures'][i]['LineName']
            dir = self.data['Departures'][i]['Direction']
            real_time = self.data['Departures'][i]['RealTime']
            scheduled_time = self.data['Departures'][i]['ScheduledTime']
            state = self.data['Departures'][i]['State']
            return(line, dir, real_time, scheduled_time, state)
        except:
            return ('line N/A', 'dir N/A', 'real_time N/A', 'scheduled_time N/A','state N/A')

    def get_data(self) -> dict:
        return self.data

def convert_utc_to_timezone(date_string, zone):
    try:
        match = re.match(r'/Date\((\d+)[+-]\d{4}\)/', date_string)
        timestamp_ms = int(match.group(1))

        utc_time = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

        time = utc_time.astimezone(pytz.timezone(zone))
        return time
    except:
        return datetime.now()

def format_datetime(time) -> str:
    hours = time.hour
    minutes = time.minute
    return f"{hours:02d}:{minutes:02d}"

def get_time_delta(time_a, time_b) -> datetime:
    delta = time_a - time_b
    minutes = int(delta.total_seconds() / 60)
    if minutes < 0:
        minutes = 0
    return f"in {minutes} Min"

if __name__ == "__main__":
    vvo = VVO()
    vvo.retrieve_stop_data('33000742')
    print(vvo.get_data())
    data = vvo.get_data_entry(0)
    time_a = convert_utc_to_timezone(data[2], 'Europe/Berlin')
    time_b = convert_utc_to_timezone(data[3], 'Europe/Berlin')
    print(time_a, time_b, get_time_delta(time_a, time_b))





#
# def get_data_time(data: str) -> datetime.time:
#     try:
#         return datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
#     except:
#         return datetime.datetime.now()
#
#
# def convert_dotnet_date(dotnet_date_str: str) -> datetime.datetime:
#     """Convert .NET Date format to Python datetime"""
#     if not dotnet_date_str or dotnet_date_str == 'undefined':
#         return None
#
#     match = re.search(r'/Date\((\d+)([+-]\d{4})\)/', dotnet_date_str)
#     if not match:
#         return None
#
#     try:
#         timestamp_ms = int(match.group(1))
#         offset_str = match.group(2)
#         timestamp_seconds = timestamp_ms / 1000.0
#         utc_datetime = datetime.datetime.fromtimestamp(
#             timestamp_seconds,
#             tz=datetime.timezone.utc
#         )
#         offset_hours = int(offset_str[1:3])
#         offset_minutes = int(offset_str[3:5])
#         if offset_str[0] == '-':
#             offset_hours = -offset_hours
#             offset_minutes = -offset_minutes
#         offset_minutes_total = offset_hours * 60 + offset_minutes
#         local_datetime = utc_datetime + datetime.timedelta(minutes=offset_minutes_total)
#         return local_datetime.astimezone(timezone)
#
#     except (ValueError, TypeError) as e:
#         print(f"Error parsing date {dotnet_date_str}: {e}")
#         return None
#
# def get_time_delta(time) -> datetime.datetime:
#     if not time:
#         return None
#
#     try:
#         now = datetime.datetime.now(timezone)
#         delta = time - now
#         return delta
#     except Exception as e:
#         print(f"Error calculating time difference: {e}")
#         return None
#
#
# def format_time_for_display(dt : datetime.datetime) -> str:
#     if not dt:
#         return 'N/A'
#     return dt.strftime('%H:%M')
#
# def format_deltatime_for_display(dt : datetime.timedelta) -> str:
#     if not dt:
#         return 'N/A'
#     return 'in ' + str(int(dt.total_seconds() / 60)) + ' Min'
