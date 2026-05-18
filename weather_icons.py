import requests
import customtkinter as customtkinter
from PIL import Image
from io import BytesIO

class WeatherIcons():
    def __init__(self):
        self.icons = self.retreive_weather_icons()

    def retreive_weather_icons(self) -> dict:
        url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"

        response = {}

        try:
            response = requests.get(url, timeout=10)

        except requests.exceptions.ConnectionError:
            print("No internet connection.")

        except requests.exceptions.Timeout:
            print("Request timed out.")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")

        except requests.exceptions.RequestException as e:
            # catches all other requests-related errors
            print(f"Request failed: {e}")
        response = response.json()
        icons = {}
        for code in response:
            img_day = self.download_weather_image(response, code, 'day')
            img_night = self.download_weather_image(response, code, 'night')
            icons[code] = [img_day, img_night]
        return icons

    def get_data(self):
        return self.icons

    def download_weather_image(self, data : {}, code : str, time: str) -> Image.Image:
        url = data[code][time]['image']
        try:
            response = requests.get(url, timeout=10)
            img_data = response.content
            return Image.open(BytesIO(img_data))

        except requests.exceptions.ConnectionError:
            print("No internet connection.")

        except requests.exceptions.Timeout:
            print("Request timed out.")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")

        except requests.exceptions.RequestException as e:
            # catches all other requests-related errors
            print(f"Request failed: {e}")

    def get_weather_image(self, code : str, res : int = 64) -> customtkinter.CTkImage:
        image_day = self.icons[code][0]
        image_night = self.icons[code][1]

        image_day = crop_image(image_day, 10)
        image_night = crop_image(image_night, 10)

        ctk_image = customtkinter.CTkImage(
            light_image=image_day,
            dark_image=image_night,
            size=(res, res))

        return ctk_image

def crop_image(image : Image.Image, crop) -> Image.Image:
    w, h = image.size
    left = crop
    right = w - crop
    upper = crop
    lower = h-crop
    return image.crop((left, upper, right, lower))

if __name__ == "__main__":
    weather_icons = WeatherIcons()
    icons = weather_icons.get_data()
    weather_image = weather_icons.get_weather_image('95', 64)
    print(weather_image)