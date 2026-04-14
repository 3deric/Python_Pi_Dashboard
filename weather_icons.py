import requests
import customtkinter as customtkinter
from PIL import Image
from io import BytesIO

class WeatherIcons():
    def __init__(self):
        self.icons = self.retreive_weather_icons()

    def retreive_weather_icons(self) -> dict:
        url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"
        response = requests.get(url)
        return response.json()

    def get_data(self):
        return self.icons

    def get_weather_image(self, code : str, res : int = 64) -> customtkinter.CTkImage:
        url_day = self.icons[code]['day']['image']
        url_night = self.icons[code]['night']['image']
        response_day = requests.get(url_day)
        response_night = requests.get(url_night)
        img_data_day = response_day.content
        img_data_night = response_night.content
        image_day = Image.open(BytesIO(img_data_day))
        image_night = Image.open(BytesIO(img_data_night))

        ctk_image = customtkinter.CTkImage(
            light_image=image_day,
            dark_image=image_night,
            size=(res, res))

        return ctk_image

if __name__ == "__main__":
    weather_icons = WeatherIcons()
    # icons = weather_icons.get_data()
    # for code in icons:
    #     print(weather_icons.get_weather_image(str(code)))