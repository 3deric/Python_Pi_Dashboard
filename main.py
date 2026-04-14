import tkinter
from unittest.mock import DEFAULT

import customtkinter
from PIL.ImageOps import pad
from customtkinter import CTkButton
from PIL import Image
from datetime import datetime, timedelta

import weather_icons
import vvo_data
import weather_data
from vvo_data import get_time_delta

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme("blue")

PADDING = 5
PADDING_TEXT = 8
DEFAULT_FONT = ('Arial', 16)
DEFAULT_FONT_BOLD = ('Arial', 16, 'bold')
CLOCK_FONT = ('Arial', 72, 'bold')
WEATHER_FONT = ('Arial', 48, 'bold')
WEATHER_DAY_FONT = ('Arial', 20, 'bold')
WEATHER_DAY_IMAGE_SIZE = 96
WEATHER_FORECAST_IMAGE_SIZE = 48
TAB_FONT =('Arial', 20)
DEP_FONT_BOLD =('Arial', 16, 'bold')
DEP_FONT_REG =('Arial', 16)
PUBLIC_TRANSPORT_ENTRIES = 7
TRANSPORT_ENTRY_CUTOFF = 25
STOP_ID = 33000028
LAT = 51.0509
LONG = 13.7383

icons = None

class CurrentDayFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width= 1)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_time = customtkinter.CTkLabel(self, text='Current Time', font= CLOCK_FONT)
        self.current_time.grid(row=0, column=0, sticky='nsew', padx=PADDING_TEXT, pady=(PADDING_TEXT,0))

        self.current_day = customtkinter.CTkLabel(self, text='Current Day', font=DEFAULT_FONT)
        self.current_day.grid(row=1, column=0, padx=PADDING_TEXT, pady=(0,PADDING_TEXT))

    def update_current_day(self):
        now = datetime.now()
        current_time = str(now.hour) + ':' + str(now.minute).zfill(2)
        current_day = now.strftime("%A") + ' ' + str(now.day) + '. ' + now.strftime("%B") + ', ' + str(now.year)
        self.current_time.configure(text = current_time)
        self.current_day.configure(text = current_day) #Saturday, March 28, 2026'

class CurrentWeatherFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width= 1)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight=5)

        self.grid_propagate(False)

        self.current_weather = CurrentWeatherView(self)
        self.current_weather.grid(column = 0, row = 0, sticky = 'nsew', columnspan = 3, padx=4, pady=(4,0))

        seperator = Seperator(self)
        seperator.grid(column =0, row = 0, sticky='sew', columnspan =3, padx=0, pady=0)

        self.weather_forecast = []

        for i in range(0,3):
            fc = WeatherForecastView(self)
            fc.grid(column = i, row = 1, sticky = 'nsew', padx=4, pady=4)
            if i < 2:
                fc.grid(padx=(4,0))
                fc_seperator = Seperator(self)
                fc_seperator.grid(column=i, row=1, sticky='nse', padx=0, pady=0)
            self.weather_forecast.append(fc)

    def set_weather_frame(self, weather : weather_data.WeatherData):
        self.current_weather.set_current_weather_view((weather.get_current_temperature(),
                                                      icons.get_weather_image(weather.get_current_weather_code(), WEATHER_DAY_IMAGE_SIZE),
                                                      weather.get_current_min_max_temp(),
                                                      weather.get_current_relative_humidity()))

        today = datetime.today()
        for i, fc in enumerate(self.weather_forecast):
            next_day = today + timedelta(days=i)
            fc.set_forecast_weather_view((next_day.strftime("%A")[:2],
                                         icons.get_weather_image(weather.get_forecast_weather_code(i + 1), WEATHER_FORECAST_IMAGE_SIZE),
                                         weather.get_forecast_min_max_temp(i +1)))

class CurrentWeatherView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 0, fg_color='transparent')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 5)
        self.grid_rowconfigure(1, weight=1)

        self.current_temp = customtkinter.CTkLabel(self, text='10°C', font=WEATHER_FONT)
        self.current_icon = customtkinter.CTkLabel(self, text='', image = icons.get_weather_image('3', WEATHER_DAY_IMAGE_SIZE), font=WEATHER_FONT)
        self.today_temps = customtkinter.CTkLabel(self, text = '10 to 15 °C', font = DEFAULT_FONT)
        self.current_humidity = customtkinter.CTkLabel(self, text = '70 % rH', font = DEFAULT_FONT)

        self.current_temp.grid(row=0, column=0, sticky='nw', padx=PADDING_TEXT, pady=PADDING_TEXT)
        self.current_icon.grid(row=0, column=1, sticky='ne', padx=0, pady=0)
        self.today_temps.grid(row=1, column=0, sticky='sw', padx=PADDING_TEXT, pady=(0,PADDING_TEXT))
        self.current_humidity.grid(row=1, column=1, sticky='se', padx=PADDING_TEXT, pady=(0,PADDING_TEXT))


    def set_current_weather_view(self, next):
        self.current_temp.configure(text = next[0])
        self.current_icon.configure(text = '', image= next[1])
        self.today_temps.configure(text = next[2])
        self.current_humidity.configure(text = next[3])

class WeatherForecastView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 0, fg_color = 'transparent')
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)

        self.fc_day = customtkinter.CTkLabel(self, text='Mo', font=WEATHER_DAY_FONT)
        self.fc_icon = customtkinter.CTkLabel(self, text='', image = icons.get_weather_image('3', WEATHER_FORECAST_IMAGE_SIZE) ,font=DEFAULT_FONT)
        self.fc_range = customtkinter.CTkLabel(self, text='10 °C\n-\n16 °C', font=DEFAULT_FONT)

        self.fc_day.grid(row=0, column=0, sticky='ew', padx=PADDING_TEXT, pady=(PADDING_TEXT,0))
        self.fc_icon.grid(row=1, column=0, sticky='ew', padx=0, pady=0)
        self.fc_range.grid(row=2, column=0, sticky='ew', padx=PADDING_TEXT, pady=(0,PADDING_TEXT))

    def set_forecast_weather_view(self, next):
        self.fc_day.configure(text = next[0])
        self.fc_icon.configure(text= '', image = next[1])
        self.fc_range.configure(text = next[2][0] + '\nto\n' + next[2][1])

class PublicTransportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 1) # , fg_color = 'transparent'

        self.grid_columnconfigure(0, weight=1)
        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            self.grid_rowconfigure(i, weight=1)

        self.entries = []

        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            entry = TransportEntryFrame(self, i)
            entry.grid(row = i, column = 0, sticky='nsew', padx=PADDING_TEXT, pady=PADDING_TEXT)
            #if i < PUBLIC_TRANSPORT_ENTRIES - 1:
            #    entry.grid(pady = (0, PADDING))

            if i < PUBLIC_TRANSPORT_ENTRIES - 1:
                seperator = Seperator(self)
                seperator.grid(sticky='new', padx=0, pady=0)
            self.entries.append(entry)

    def set_transport_entries(self):
        vvo.retrieve_stop_data()
        print('Retrieving VVO Data')
        print(vvo.get_data())
        for i, e in enumerate(self.entries):
            e.set_transport_entry(vvo.get_data_entry(i))

class TransportEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master, i : int):
        super().__init__(master, fg_color= 'transparent')

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_propagate(False)

        self.line = customtkinter.CTkLabel(self, text='Line', font=DEP_FONT_BOLD)
        self.state = customtkinter.CTkLabel(self, text='State', font=DEP_FONT_REG)
        self.time_real= customtkinter.CTkLabel(self, text='Delta Time', font=DEP_FONT_BOLD)
        self.time_sched = customtkinter.CTkLabel(self, text='Scheduled Time', font=DEP_FONT_REG)

        self.line.grid(row=0, column=0, sticky='nw', padx =0, pady = 0)
        self.state.grid(row=1, column=0, sticky='sw', padx=0, pady=0)
        self.time_real.grid(row=0, column=1, sticky='ne', padx=0, pady=0)
        self.time_sched.grid(row=1, column=1, sticky='se', padx=0, pady=0)

    def set_transport_entry(self, next : tuple):
        print(next)
        line_dir = (next[1][:TRANSPORT_ENTRY_CUTOFF] + '..') if len(next[1]) > TRANSPORT_ENTRY_CUTOFF else next[1]
        line_time_sched = vvo_data.convert_utc_to_timezone(next[3])
        line_time_real = get_time_delta(vvo_data.convert_utc_to_timezone(next[2]))
        self.line.configure(text = next[0] + ' ' + line_dir)
        self.state.configure(text = next[4][:10])
        self.time_real.configure(text = line_time_real)
        self.time_sched.configure(text = str(line_time_sched.hour) + ':' + str(line_time_sched.minute).zfill(2))

class TabViewFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, bg_color='transparent', border_width= 1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bg_color= 'transparent', fg_color= 'transparent')

        tab_transport = self.add('Public Transport')
        tab_weather = self.add('Weather')
        tab_calendar = self.add('Calendar')

        self.transport_image = customtkinter.CTkImage(light_image=Image.open('img/directions_bus_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    dark_image=Image.open('img/directions_bus_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    size=(24, 24))
        self.weather_image = customtkinter.CTkImage(light_image=Image.open('img/cloud_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    dark_image=Image.open('img/cloud_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    size=(24, 24))
        self.calendar_image = customtkinter.CTkImage(light_image=Image.open('img/calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    dark_image=Image.open('img/calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    size=(24, 24))

        self.transport_button = self._segmented_button._buttons_dict['Public Transport']
        self.weather_button = self._segmented_button._buttons_dict['Weather']
        self.calendar_button = self._segmented_button._buttons_dict['Calendar']
        self.transport_button.configure(font=TAB_FONT, image = self.transport_image, text = 'Public Transport')
        self.weather_button.configure(font=TAB_FONT, image = self.weather_image, text = 'Weather')
        self.calendar_button.configure(font=TAB_FONT, image = self.calendar_image, text = 'Calendar')

class Seperator(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height = 2, width = 2, border_width= 1, corner_radius=0)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Pi Dashboard')
        self.geometry('800x480')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.grid_rowconfigure(0, weight=1)  #
        self.grid_rowconfigure(1, weight=10)

        self.current_day = CurrentDayFrame(self)
        self.current_day.grid(column=0, row=0, padx = PADDING, pady= PADDING, sticky='nsew')

        self.current_day.update_current_day()

        self.current_weather_frame = CurrentWeatherFrame(self)
        self.current_weather_frame.grid(column=0, row=1, padx = PADDING, pady = (0,PADDING), sticky='nsew')

        #button = CTkButton(self.current_day, command = self.set_update_data, text = 'Update Data')
        #button.grid(column = 0, row = 2, padx = 20, pady = 20)

        #self.tab_view_frame = TabViewFrame(self)
        #self.tab_view_frame.grid(column = 1, row = 0, rowspan = 2, padx = (0, PADDING), pady = (PADDING), sticky = 'nsew')

        #self.tab_view = TabView(self.tab_view_frame)
        #self.tab_view = TabView(self)
        #self.tab_view.grid(column = 1, row = 0, rowspan = 2, padx = (0, PADDING), pady = (PADDING), sticky = 'nsew')

        #self.public_transport = PublicTransportFrame(self.tab_view.tab('Public Transport'))
        self.public_transport = PublicTransportFrame(self)
        self.public_transport.grid(column = 1, row = 0, rowspan = 2, padx = (0, PADDING), pady = (PADDING), sticky = 'nsew')
        #self.public_transport.pack(expand=True, fill='both')

        self.set_update_data()

    def set_update_data(self):
        self.public_transport.set_transport_entries()
        self.set_weather_panel()

    def set_weather_panel(self):
        weather.retrieve_data()

        self.current_weather_frame.set_weather_frame((weather))
        # print(f"Current temperature_2m: {weather.get_current_temperature()}")
        # print(f"Current relative_humidity_2m: {weather.get_current_relative_humidity()}")
        # print(f"Current weather_code: {weather.get_current_weather_code()}")
        # print(f"Current wind_speed_10m: {weather.get_current_wind_speed_10m()}")
        # print(f"Current wind_direction_10m: {weather.get_current_wind_direction_10m()}")
        # print(f"Current precipitation: {weather.get_current_precipitation()}")

    def set_weather_entries(self):
        pass

if __name__ == "__main__":
    icons = weather_icons.WeatherIcons()
    vvo = vvo_data.VVOData(STOP_ID)
    weather = weather_data.WeatherData(LAT, LONG)
    app = App()
    app.mainloop()




