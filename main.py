import customtkinter
from customtkinter import CTkButton

import vvo_data

customtkinter.set_appearance_mode('Dark')

PADDING = 10
PADDING_TEXT = 5
TAB_FONT =('Arial', 20)
DEP_FONT_BOLD =('Arial', 14, 'bold')
DEP_FONT_REG =('Arial', 14)
PUBLIC_TRANSPORT_ENTRIES = 7
TRANSPORT_ENTRY_CUTOFF = 25
TIMEZONE = 'Europe/Berlin'

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

class CurrentDayWeatherFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self._border_width = 1

class PublicTransportFrame(customtkinter.CTkFrame):
    def __init__(self, master, stop_id):
        super().__init__(master, border_width = 1)

        self.grid_columnconfigure(0, weight=1)
        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            self.grid_rowconfigure(i, weight=1)

        self.stop_id = stop_id
        self.entries = []

        for i in range(PUBLIC_TRANSPORT_ENTRIES):
            entry = TransportEntryFrame(self, i)
            entry.grid(row = i, column = 0, sticky='nsew', padx = 2, pady = 2)
            self.entries.append(entry)

        self.vvo = vvo_data.VVO()

    def set_transport_entries(self):
        self.vvo.retrieve_stop_data(self.stop_id)
        print("Retrieving VVO Data")
        print(self.vvo.get_data())
        for i, e in enumerate(self.entries):
            e.set_transport_entry(self.vvo.get_data_entry(i))

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
        self.time_real= customtkinter.CTkLabel(self, text='Realtime', font=DEP_FONT_BOLD)
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

        self.current_weather = CurrentDayWeatherFrame(self)
        self.current_weather.grid(column=0, row=1, padx = PADDING, pady = (0,PADDING), sticky='nsew')

        button = CTkButton(self.current_day, command = self.set_update_data, text = 'Update Data')
        button.grid(column = 0, row = 2, padx = 20, pady = 20)

        self.public_transport = PublicTransportFrame(self, 33000028)
        self.public_transport.grid(column=1, row=0, rowspan=2, padx=(0,PADDING), pady=(PADDING), sticky='nsew')

    def set_update_data(self):
        self.public_transport.set_transport_entries()

app = App()
app.mainloop()





# class TabView(customtkinter.CTkTabview):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#
#         self._anchor = 'n'
#         self._border_width = 1
#
#         self.add('Public Transport')
#         self.add('Weather')
#
#         for button in self._segmented_button._buttons_dict.values():
#             button.configure(font=TAB_FONT)  # Change font using font object
#             # button.configure(text='Change Text of Button')
#
#         self.entries = []
#         for i in range(20):
#             entry = customtkinter.CTkLabel(master=self.tab('Public Transport'))
#             entry.grid(row=i, column = 0, padx=10, pady=5, sticky = 'nsew')
#             self.entries.append(entry)