import time
import pytz
import requests
from datetime import datetime, timezone, timedelta
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TIMEZONE = 'Europe/Berlin'

class VVOData:
    def __init__(self, stopid: str):
        self.timezone = pytz.timezone("Europe/Berlin")
        self.stopid = stopid
        self.data = {}

        self.session = requests.Session()

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            status=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retry,
            pool_connections=1,
            pool_maxsize=1,
        )

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.url = "https://webapi.vvo-online.de/dm"

        self.attributes = {
            "stopid": self.stopid,
            "limit": 10,
            "mot": [
                "Tram",
                "CityBus",
                "IntercityBus",
                "SuburbanRailway",
                "Train",
                "Cableway",
                "Ferry",
                "HailedSharedTaxi",
            ],
        }

    def retrieve_stop_data(self):
        start = time.monotonic()

        try:
            response = self.session.post(
                self.url,
                json=self.attributes,
                timeout=(10, 30),
            )

            elapsed = time.monotonic() - start

            response.raise_for_status()
            data = response.json()
            self.data = data

            print(
                f"VVO request successful: "
                f"stop={self.stopid}, "
                f"time={elapsed:.2f}s"
            )
            return True

        except requests.exceptions.Timeout:
            print(
                f"VVO request timed out: "
                f"stop={self.stopid}"
            )

        except requests.exceptions.ConnectionError as e:
            print(
                f"VVO connection error: "
                f"stop={self.stopid}: {e}"
            )

        except requests.exceptions.HTTPError as e:
            print(
                f"VVO HTTP error: "
                f"stop={self.stopid}, "
                f"status={response.status_code}: {e}"
            )

        except ValueError as e:
            print(
                f"VVO returned invalid JSON: "
                f"stop={self.stopid}: {e}"
            )

        except requests.exceptions.RequestException as e:
            print(
                f"VVO request failed: "
                f"stop={self.stopid}: {e}"
            )

        except Exception as e:
            print(
                f"Unexpected error retrieving VVO data: "
                f"stop={self.stopid}: {e}"
            )
        return False

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

def convert_utc_to_timezone(date_string):
    try:
        match = re.match(r'/Date\((\d+)[+-]\d{4}\)/', date_string)
        timestamp_ms = int(match.group(1))

        utc_time = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

        time = utc_time.astimezone(pytz.timezone(TIMEZONE))
        return time
    except:
        return datetime.now()

def format_datetime(time) -> str:
    hours = time.hour
    minutes = time.minute
    return f"{hours:02d}:{minutes:02d}"

def get_time_delta(time) -> str:
    tz = pytz.timezone(TIMEZONE)
    if time.tzinfo is None:
        time = tz.localize(time)
    now = datetime.now(tz)
    delta = time - now
    minutes = int(delta.total_seconds() / 60)
    if minutes < 0:
        minutes = 0
    return f"in {minutes} Min"

if __name__ == "__main__":
    vvo = VVOData('33000742')
    vvo.retrieve_stop_data()
    print(vvo.get_data())
    data = vvo.get_data_entry(0)
    time = convert_utc_to_timezone(data[3])
    print(get_time_delta(time))
    #print(time_b, time_a, get_time_delta(time_a, time_b))