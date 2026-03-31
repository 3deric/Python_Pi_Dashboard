import requests

class WeatherIcons():
    def __init__(self):
        self.icons = self.retreive_weather_icons()

    def retreive_weather_icons(self) -> dict:
        url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"
        response = requests.get(url)
        return response.json()

    def get_data(self):
        return self.icons

    def get_weather_image(self, code : str, type : str = 'day') -> str:
        return self.icons[code][type]['image']

if __name__ == "__main__":
    weather_icons = WeatherIcons()
    icons = weather_icons.get_data()

    for code in icons:
        print(weather_icons.get_weather_image(str(code)))