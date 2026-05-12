# Python Pi Dashboard

Second version of my raspberry pi dashboard. A desktop application made with custom tkinter.
![Python Dashboard Preview](/preview.png)
![Python Dashboard Weather Preview](/preview_weather.png)
# Setup
## Hardware Requirements
The dashboard is meant to be used with the 800 x 480 Pixel version of the raspberry-pi Touchscreen. Font sizes and all UI elements are optimized for this display.

## After cloning the repository it is important to create a virtual environment.
Open a terminal inside of the repository and execute the following command.

```
python -m venv venv
```

Then install all the dependencies with pip.
```
./bin/pip install requirements.txt
```

Then you can execute the application with.
```
./bin/python main.py
```


## Setting Weather and Public Transport
Weather location and the public transport stop can be set in `config.py`. 
```
STOP_ID = 33000028
LOCATION = (51.0509, 13.7383)
```

## Font Sizes and Style
Fonts can be adjusted in `style.py`. The amount of displayed transport and weather forecast panels can be set too. Be aware that this might require changes to the requests. The requests only gather a limited amount of information.
```
PADDING_TEXT = 8
DEFAULT_FONT = ('Piboto', 16)
DEFAULT_FONT_BOLD = ('Piboto', 16, 'bold')
CLOCK_FONT = ('Piboto', 72, 'bold')
WEATHER_FONT = ('Piboto', 48, 'bold')
WEATHER_DAY_FONT = ('Piboto', 20, 'bold')
WEATHER_DAY_IMAGE_SIZE = 96
WEATHER_FORECAST_IMAGE_SIZE = 48
TAB_FONT =('Piboto', 20)
FORECAST_FONT_BOLD =('Piboto', 16, 'bold')
FORECAST_FONT_REG =('Piboto', 16)
FORECAST_FONT_LIGHT =('Piboto', 10)
PUBLIC_TRANSPORT_ENTRIES = 7
WEATHER_FORECAST_ENTRIES = 7
TRANSPORT_ENTRY_CUTOFF = 25
```