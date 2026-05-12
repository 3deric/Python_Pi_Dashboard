import customtkinter
from PIL import Image
from datetime import datetime, timedelta

from pandas.core.interchange import column

import weather_icons
import vvo_data
import weather_data
import style
import config
from vvo_data import get_time_delta

icons = None

class CurrentDayFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 1,
                         width=100,
                         height=150)

        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_time = customtkinter.CTkLabel(self, text='23:59', font= style.CLOCK_FONT)
        self.current_time.grid(row=0, column=0, sticky='nsew', padx=style.PADDING_TEXT, pady=(style.PADDING_TEXT,0))

        self.current_day = customtkinter.CTkLabel(self, text='Current Day', font=style.DEFAULT_FONT)
        self.current_day.grid(row=1, column=0, padx=style.PADDING_TEXT, pady=(0,style.PADDING_TEXT))

        self.update()

    def update_current_day(self):
        now = datetime.now()
        current_time = str(now.hour) + ':' + str(now.minute).zfill(2)
        current_day = now.strftime("%A") + ' ' + str(now.day) + '. ' + now.strftime("%B") + ', ' + str(now.year)
        self.current_time.configure(text = current_time)
        self.current_day.configure(text = current_day)

    def update(self):
        self.update_current_day()
        self.master.after(1000, self.update)

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
        seperator.grid(column =0, row = 0, sticky='sew', columnspan =3, padx=5, pady=0)

        self.weather_forecast = []

        for i in range(0,3):
            fc = WeatherForecastView(self)
            fc.grid(column = i, row = 1, sticky = 'nsew', padx=5, pady=5)
            if i < 2:
                fc.grid(padx=(4,0))
                fc_seperator = Seperator(self)
                fc_seperator.grid(column=i, row=1, sticky='nse', padx=5, pady=5)
            self.weather_forecast.append(fc)

        self.update()

    def set_weather_frame(self, weather : weather_data.WeatherData):
        self.current_weather.set_current_weather_view((weather.get_current_temperature(),
                                                      icons.get_weather_image(weather.get_current_weather_code(), style.WEATHER_DAY_IMAGE_SIZE),
                                                      weather.get_current_min_max_temp(),
                                                      weather.get_current_precipitation_propability()))

        today = datetime.today()
        for i, fc in enumerate(self.weather_forecast):
            next_day = today + timedelta(days=i + 1)
            fc.set_forecast_weather_view((next_day.strftime("%A")[:2],
                                         icons.get_weather_image(weather.get_forecast_weather_code(i + 1), style.WEATHER_FORECAST_IMAGE_SIZE),
                                         weather.get_forecast_min_max_temp(i +1)))

    def update(self):
        weather.retrieve_data()
        self.set_weather_frame(weather)
        self.master.after(1800000 , self.update)

class CurrentWeatherView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 0, fg_color='transparent')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 5)
        self.grid_rowconfigure(1, weight=1)

        self.current_temp = customtkinter.CTkLabel(self, text='-30 °C', font=style.WEATHER_FONT)
        self.current_icon = customtkinter.CTkLabel(self, text='', image = icons.get_weather_image('3', style.WEATHER_DAY_IMAGE_SIZE), font=style.WEATHER_FONT)
        self.today_temps = customtkinter.CTkLabel(self, text = '10.1 / 15.1 °C', font = style.DEFAULT_FONT)
        self.current_rain_propability = customtkinter.CTkLabel(self, text = '☔ 70 %', font = style.DEFAULT_FONT)

        self.current_temp.grid(row=0, column=0, sticky='nw', padx=style.PADDING_TEXT, pady=style.PADDING_TEXT)
        self.current_icon.grid(row=0, column=1, sticky='ne', padx=0, pady=0)
        self.today_temps.grid(row=1, column=0, sticky='sw', padx=style.PADDING_TEXT, pady=(0,style.PADDING_TEXT))
        self.current_rain_propability.grid(row=1, column=1, sticky='se', padx=style.PADDING_TEXT, pady=(0,style.PADDING_TEXT))


    def set_current_weather_view(self, next):
        self.current_temp.configure(text = next[0])
        self.current_icon.configure(text = '', image= next[1])
        self.today_temps.configure(text = next[2])
        self.current_rain_propability.configure(text = '☂ ' + next[3])

class WeatherForecastView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 0, fg_color = 'transparent')
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)

        self.fc_day = customtkinter.CTkLabel(self, text='Mo', font=style.WEATHER_DAY_FONT)
        self.fc_icon = customtkinter.CTkLabel(self, text='', image = icons.get_weather_image('3', style.WEATHER_FORECAST_IMAGE_SIZE) ,font=style.DEFAULT_FONT)
        self.fc_range = customtkinter.CTkLabel(self, text='10.5 °C\n-\n16.5 °C', font=style.DEFAULT_FONT)

        self.fc_day.grid(row=0, column=0, sticky='ew', padx=style.PADDING_TEXT, pady=(style.PADDING_TEXT,0))
        self.fc_icon.grid(row=1, column=0, sticky='ew', padx=0, pady=0)
        self.fc_range.grid(row=2, column=0, sticky='ew', padx=style.PADDING_TEXT, pady=(0,style.PADDING_TEXT))

    def set_forecast_weather_view(self, next):
        self.fc_day.configure(text = next[0])
        self.fc_icon.configure(text= '', image = next[1])
        self.fc_range.configure(text = next[2][0] + '\n-\n' + next[2][1])

class PublicTransportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 1) # , fg_color = 'transparent'

        self.grid_columnconfigure(0, weight=1)
        for i in range(style.PUBLIC_TRANSPORT_ENTRIES):
            self.grid_rowconfigure(i, weight=1)

        self.entries = []

        for i in range(style.PUBLIC_TRANSPORT_ENTRIES):
            entry = TransportEntryFrame(self, i)
            entry.grid(row = i, column = 0, sticky='nsew', padx=style.PADDING_TEXT, pady=style.PADDING_TEXT)
            if i < style.PUBLIC_TRANSPORT_ENTRIES - 1:
                seperator = Seperator(self)
                seperator.grid(sticky='new', padx=5, pady=0)
            self.entries.append(entry)

        self.update()

    def set_transport_entries(self):
        vvo.retrieve_stop_data()
        for i, e in enumerate(self.entries):
            e.set_transport_entry(vvo.get_data_entry(i))

    def update(self):
        self.set_transport_entries()
        self.master.after(60000, self.update)

class TransportEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master, i : int):
        super().__init__(master, fg_color= 'transparent')

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_propagate(False)

        self.line = customtkinter.CTkLabel(self, text='Line', font=style.FORECAST_FONT_BOLD)
        self.state = customtkinter.CTkLabel(self, text='State', font=style.FORECAST_FONT_REG)
        self.time_real= customtkinter.CTkLabel(self, text='Delta Time', font=style.FORECAST_FONT_BOLD)
        self.time_sched = customtkinter.CTkLabel(self, text='Scheduled Time', font=style.FORECAST_FONT_REG)

        self.line.grid(row=0, column=0, sticky='nw', padx =0, pady = 0)
        self.state.grid(row=1, column=0, sticky='sw', padx=0, pady=0)
        self.time_real.grid(row=0, column=1, sticky='ne', padx=0, pady=0)
        self.time_sched.grid(row=1, column=1, sticky='se', padx=0, pady=0)

    def set_transport_entry(self, next : tuple):
        line_dir = (next[1][:style.TRANSPORT_ENTRY_CUTOFF] + '..') if len(next[1]) > style.TRANSPORT_ENTRY_CUTOFF else next[1]
        line_time_sched = vvo_data.convert_utc_to_timezone(next[3])
        line_time_real = get_time_delta(vvo_data.convert_utc_to_timezone(next[2]))
        self.line.configure(text = next[0] + ' ' + line_dir)
        self.state.configure(text = next[4][:10])
        self.time_real.configure(text = line_time_real)
        self.time_sched.configure(text = str(line_time_sched.hour) + ':' + str(line_time_sched.minute).zfill(2))

class WeatherForecastFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width = 1) # , fg_color = 'transparent'

        self.grid_columnconfigure(0, weight=1)
        for i in range(style.WEATHER_FORECAST_ENTRIES):
            self.grid_rowconfigure(i, weight=1)

        self.entries = []

        for i in range(style.WEATHER_FORECAST_ENTRIES):
            entry = WeatherForecastEntryFrame(self, i)
            entry.grid(row = i, column = 0, sticky='nsew', padx=style.PADDING_TEXT, pady=style.PADDING_TEXT)
            if i < style.WEATHER_FORECAST_ENTRIES - 1:
                 seperator = Seperator(self)
                 seperator.grid(sticky='new', padx=5, pady=0)
            self.entries.append(entry)

        self.update()

    def set_weather_entries(self):
        today = datetime.today()
        for i, e in enumerate(self.entries):
            day = today + timedelta(days = i)
            day_name = day.strftime("%A")
            day_date = str(day.day) + '. ' + day.strftime("%B")
            e.set_weather_forecast_entry((day_name,
                                          day_date,
                                          icons.get_weather_image(weather.get_forecast_weather_code(i)),
                                          weather.get_forecast_min_max_temp(i),
                                          weather.get_forecast_wind_speed_10m(i),
                                          weather.get_forecast_precipitation_propability(i)))

    def update(self):
        self.set_weather_entries()
        self.master.after(1800000, self.update)

class WeatherForecastEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master, i : int):
        super().__init__(master, fg_color= 'transparent')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        for i, weight in enumerate((2, 2, 3, 2, 2)):
            self.grid_columnconfigure(i, weight=weight, uniform="forecast")
        self.grid_propagate(False)

        self.day = customtkinter.CTkLabel(self, text='Thursday', font=style.FORECAST_FONT_BOLD)
        self.day_date = customtkinter.CTkLabel(self, text='December 31', font=style.FORECAST_FONT_REG)
        self.current_icon = customtkinter.CTkLabel(self, text='',
                                                   image=icons.get_weather_image('3', style.WEATHER_FORECAST_IMAGE_SIZE),
                                                   font=style.WEATHER_FONT)
        self.temp = customtkinter.CTkLabel(self, text='13 °C / 21 °C', font=style.FORECAST_FONT_BOLD)
        self.wind = customtkinter.CTkLabel(self, text='🌫 20 Km/h', font=style.FORECAST_FONT_REG)
        #self.wind_dir = customtkinter.CTkLabel(self, text='NW', font = FORECAST_FONT_LIGHT)
        #self.humidity = customtkinter.CTkLabel(self, text='💧 40 %', font=style.FORECAST_FONT_BOLD)
        self.rain = customtkinter.CTkLabel(self, text='☂ 50 %', font=style.FORECAST_FONT_REG)

        self.day_sep = Seperator(self)
        self.temp_sep = Seperator(self)
        self.rain_sep = Seperator(self)

        self.day.grid(row = 0, column = 0, sticky='nsw', padx =0, pady = 0)
        self.day_date.grid(row = 1, column = 0, sticky='nsw', padx =0, pady = 0)
        self.current_icon.grid(column = 1, row = 0, columnspan =1, rowspan= 2, sticky = 'nsew', padx =style.PADDING_TEXT, pady = 0)
        self.temp.grid(column = 2, row = 0, columnspan =1, rowspan= 2, sticky = 'nsew', padx =style.PADDING_TEXT, pady = 0)
        self.wind.grid(row=0, column=3, rowspan = 2, sticky='nsew', padx=0, pady=0)
        #self.wind_dir.grid(row=1, column=3, sticky='nw', padx=0, pady=0)
        #self.humidity.grid(column = 4, row = 0, columnspan =1, rowspan= 2, sticky = 'nsew', padx =0, pady = 0)
        self.rain.grid(column = 4, row = 0, columnspan =1, rowspan= 2, sticky = 'nsew', padx = (style.PADDING_TEXT,0), pady = 0)

        self.day_sep.grid(column=2, row=0, rowspan=2, sticky='nsw', padx=0, pady=5)
        self.temp_sep.grid(column = 2, row = 0, rowspan=2, sticky='nse', padx=0, pady=5)
        self.rain_sep.grid(column=4, row =0, rowspan=2, sticky='nsw', padx=0, pady=5)

    def set_weather_forecast_entry(self, next : tuple):
        self.day.configure(text=next[0])
        self.day_date.configure(text=next[1])
        self.current_icon.configure(image=next[2])
        self.temp.configure(text=next[3][0] + ' / ' + next[3][1])
        self.wind.configure(text='🍃 ' + next[4])
        self.rain.configure(text='☔ ' + next[5])

class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, bg_color= 'transparent', fg_color= 'transparent', corner_radius=0, border_width=0)

        self.transport = self.add('Transport')
        self.weather = self.add('Weather')
        #self.calendar = self.add('Calendar')

        self.transport_image = customtkinter.CTkImage(light_image=Image.open('img/directions_bus_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    dark_image=Image.open('img/directions_bus_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    size=(24, 24))
        self.weather_image = customtkinter.CTkImage(light_image=Image.open('img/cloud_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    dark_image=Image.open('img/cloud_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
                                                    size=(24, 24))
        #self.calendar_image = customtkinter.CTkImage(light_image=Image.open('img/calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
        #                                            dark_image=Image.open('img/calendar_month_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png'),
        #                                            size=(24, 24))

        self.transport_button = self._segmented_button._buttons_dict['Transport']
        self.weather_button = self._segmented_button._buttons_dict['Weather']
        #self.calendar_button = self._segmented_button._buttons_dict['Calendar']
        self._segmented_button.grid(sticky='nsew', padx = 0, pady = 0)
        self._segmented_button.configure(corner_radius = 5, border_width = 1)
        self.transport_button.configure(font=style.TAB_FONT, image = self.transport_image, text = 'Transport')
        self.weather_button.configure(font=style.TAB_FONT, image = self.weather_image, text = 'Weather')
        #self.calendar_button.configure(font=TAB_FONT, image = self.calendar_image, text = 'Calendar')
        self._segmented_button.configure(
            fg_color=customtkinter.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            selected_color=customtkinter.ThemeManager.theme["CTkSegmentedButton"]["selected_color"],
            unselected_color=customtkinter.ThemeManager.theme["CTkSegmentedButton"]["unselected_color"],
        )

class Seperator(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height = 0, width = 0, border_width= 1, corner_radius=0, fg_color='grey70')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('Pi Dashboard')
        self.geometry('800x480')
        self.fullscreen_state = False


        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.grid_rowconfigure(0, weight=1)  #
        self.grid_rowconfigure(1, weight=10)

        self.current_day = CurrentDayFrame(self)
        self.current_day.grid(column=0, row=0, padx = (style.PADDING,style.PADDING/2), pady= style.PADDING, sticky='nsew')

        self.current_weather_frame = CurrentWeatherFrame(self)
        self.current_weather_frame.grid(column=0, row=1, padx = (style.PADDING,style.PADDING/2), pady = (0,style.PADDING), sticky='nsew')

        self.tab_view = TabView(self)
        self.tab_view.grid(column = 1, row = 0, rowspan = 2, padx = (style.PADDING/2, style.PADDING), pady = (0, style.PADDING), sticky = 'nsew')

        self.public_transport = PublicTransportFrame(self.tab_view.tab('Transport'))
        self.public_transport.pack(expand=True, fill='both', pady = (style.PADDING,0))

        self.weather_forecast = WeatherForecastFrame(self.tab_view.tab('Weather'))
        self.weather_forecast.pack(expand=True, fill='both', pady = (style.PADDING,0))
        #self.public_transport = PublicTransportFrame(self)
        #self.public_transport.grid(column = 1, row = 0, rowspan = 2, padx = (0, style.PADDING), pady = (style.PADDING), sticky = 'nsew')

    def toggle_fullscreen(self, event=None):
        self.fullscreen_state = not self.fullscreen_state  # Just toggling the boolean
        self.attributes('-fullscreen', self.fullscreen_state)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen_state = False
        self.attributes('-fullscreen', self.fullscreen_state)
        return "break"

if __name__ == "__main__":
    icons = weather_icons.WeatherIcons()
    vvo = vvo_data.VVOData(config.STOP_ID)
    weather = weather_data.WeatherData(config.LOCATION[0], config.LOCATION[1])
    customtkinter.set_appearance_mode('light')
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()




