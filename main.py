import customtkinter
from PIL.Image import alpha_composite
from customtkinter import CTkButton
from PIL import Image

import vvo_data
import weather_data

customtkinter.set_appearance_mode('Dark')

PADDING = 10
PADDING_TEXT = 5
TAB_FONT =('Arial', 20)
DEP_FONT_BOLD =('Arial', 14, 'bold')
DEP_FONT_REG =('Arial', 14)
PUBLIC_TRANSPORT_ENTRIES = 7
TRANSPORT_ENTRY_CUTOFF = 25
TIMEZONE = 'Europe/Berlin'
STOP_ID = 33000028
LAT = 51.0509
LONG = 13.7383

class CurrentDayFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._border_width = 1

        self.current_time = customtkinter.CTkLabel(self, text='Current Time', font=('Arial', 48))
        self.current_time.grid(row=0, column=0, sticky='nsew', padx=PADDING_TEXT, pady=(PADDING_TEXT,0))

        self.current_day = customtkinter.CTkLabel(self, text='Current Day', font=('Arial', 18))
        self.current_day.grid(row=1, column=0, padx=PADDING_TEXT, pady=(0,PADDING_TEXT))

    def update_current_day(self):
        self.current_time.configure(text = '17:36')
        self.current_day.configure(text = 'Saturday, March 28, 2026')

class CurrentWeatherFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self._border_width = 1
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight=1)

class CurrentWeatherView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color = 'green')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight=1)

        self.current_temp = customtkinter.CTkLabel(self, text='10°C', font=('Arial', 20))
        self.today_temps = customtkinter.CTkLabel(self, text = '10 to 15 °C')
        self.current_humidity = customtkinter.CTkLabel(self, text = '70 % rH')

        self.current_temp.grid(row=0, column=0, sticky='nw', padx=PADDING_TEXT, pady=0)
        self.today_temps.grid(row=1, column=0, sticky='sw', padx=PADDING_TEXT, pady=0)
        self.current_humidity.grid(row=1, column=1, sticky='se', padx=PADDING_TEXT, pady=0)

    def set_current_weather_view(self, next):
        self.current_temp.configure(text = next[0])
        self.today_temps.configure(text = next[1])
        self.current_humidity.configure(text = next[2])

class PublicTransportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color = 'transparent')

        self.grid_columnconfigure(0, weight=1)
        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            self.grid_rowconfigure(i, weight=1)

        self.entries = []

        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            entry = TransportEntryFrame(self, i)
            entry.grid(row = i, column = 0, sticky='nsew', padx = 0, pady = 0)
            self.entries.append(entry)

class TransportEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master, i : int):
        super().__init__(master, bg_color='transparent', fg_color= 'transparent')

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_propagate(False)

        self.line = customtkinter.CTkLabel(self, text='Line', font=DEP_FONT_BOLD)
        self.state = customtkinter.CTkLabel(self, text='State', font=DEP_FONT_REG)
        self.time_real= customtkinter.CTkLabel(self, text='Delta Time', font=DEP_FONT_BOLD)
        self.time_sched = customtkinter.CTkLabel(self, text='Scheduled Time', font=DEP_FONT_REG)

        self.line.grid(row=0, column=0, sticky='nw', padx=PADDING_TEXT, pady=0)
        self.state.grid(row=1, column=0, sticky='sw', padx=PADDING_TEXT, pady=0)
        self.time_real.grid(row=0, column=1, sticky='ne', padx=PADDING_TEXT, pady=0)
        self.time_sched.grid(row=1, column=1, sticky='se', padx=PADDING_TEXT, pady=0)

        if i < PUBLIC_TRANSPORT_ENTRIES -1:
            seperator = Seperator(self)
            seperator.grid(sticky='nsew', columnspan =2, padx=0, pady=0)

    def set_transport_entry(self, next : tuple):
        print(next)
        line_dir = (next[1][:TRANSPORT_ENTRY_CUTOFF] + '..') if len(next[1]) > TRANSPORT_ENTRY_CUTOFF else next[1]
        line_time_sched = vvo_data.convert_utc_to_timezone(next[3], TIMEZONE)
        line_time_real = vvo_data.convert_utc_to_timezone(next[2], TIMEZONE)
        self.line.configure(text = next[0] + ' ' + line_dir)
        self.state.configure(text = next[4][:10])
        self.time_real.configure(text = line_time_real)
        self.time_sched.configure(text = line_time_sched)

class TabViewFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, bg_color='transparent', border_width= 1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._border_width = 1

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
        super().__init__(master, height = 2, width = 2)
        self._border_width = 1
        self._corner_radius = 0

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Pi Dashboard')
        self.geometry('800x480')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.grid_rowconfigure(0, weight=1)  #
        self.grid_rowconfigure(1, weight=3)

        self.current_day = CurrentDayFrame(self)
        self.current_day.grid(column=0, row=0, padx = PADDING, pady= PADDING, sticky='nsew')

        self.current_day.update_current_day()

        self.current_weather_frame = CurrentWeatherFrame(self)
        self.current_weather_frame.grid(column=0, row=1, padx = PADDING, pady = (0,PADDING), sticky='nsew')

        self.current_weather = CurrentWeatherView(self.current_weather_frame)
        self.current_weather.grid(column = 0, row = 0, sticky = 'nsew')
        self.current_weather2 = CurrentWeatherView(self.current_weather_frame)
        self.current_weather2.grid(column = 0, row = 1, sticky = 'nsew')

        button = CTkButton(self.current_day, command = self.set_update_data, text = 'Update Data')
        button.grid(column = 0, row = 2, padx = 20, pady = 20)

        self.tab_view_frame = TabViewFrame(self)
        self.tab_view_frame.grid(column = 1, row = 0, rowspan = 2, padx = (0, PADDING), pady = (PADDING), sticky = 'nsew')

        self.tab_view = TabView(self.tab_view_frame)
        self.tab_view.grid(column=0, row=0, padx = 2, pady = 2,sticky = 'nsew')

        self.public_transport = PublicTransportFrame(self.tab_view.tab('Public Transport'))
        self.public_transport.pack(expand=True, fill='both')

        #self.tab_view = TabView(self)
        #self.tab_view.grid(column = 1, row = 0, rowspan = 2, padx = (0, PADDING), pady = (PADDING), sticky = 'nsew')

        #self.public_transport = PublicTransportFrame(self.tab_view, 33000028)
        #self.public_transport.grid(column=1, row=0, rowspan=2, padx=(0,PADDING), pady=(PADDING), sticky='nsew')

    def set_update_data(self):
        self.set_transport_entries()
        self.set_weather_panel()

    def set_transport_entries(self):
        vvo.retrieve_stop_data()
        print('Retrieving VVO Data')
        print(vvo.get_data())
        for i, e in enumerate(self.public_transport.entries):
            e.set_transport_entry(vvo.get_data_entry(i))

    def set_weather_panel(self):
        weather.retrieve_data()

        self.current_weather.set_current_weather_view((weather.get_current_temperature(),
                                                       weather.get_current_min_max_temp(),
                                                       weather.get_current_relative_humidity()))
        print(f"Current temperature_2m: {weather.get_current_temperature()}")
        print(f"Current relative_humidity_2m: {weather.get_current_relative_humidity()}")
        print(f"Current weather_code: {weather.get_current_weather_code()}")
        print(f"Current wind_speed_10m: {weather.get_current_wind_speed_10m()}")
        print(f"Current wind_direction_10m: {weather.get_current_wind_direction_10m()}")
        print(f"Current precipitation: {weather.get_current_precipitation()}")

    def set_weather_entries(self):
        pass

if __name__ == "__main__":
    vvo = vvo_data.VVOData(STOP_ID)
    weather = weather_data.WeatherData(LAT, LONG)
    app = App()
    app.mainloop()




