from nicegui import ui
import vvo_data

box_colors = ['bg-blue-100', 'bg-green-100', 'bg-yellow-100', 'bg-red-100', 'bg-purple-100']
dep_data = vvo_data.get_vvo_data('33000028')
print(dep_data)

with ui.column().classes('w-full p-4 gap-2'):
    ui.label('Departures').classes('text-2xl font-bold mb-4')

    for i in range(10):
        with ui.card().classes(f'w-full h-16 {box_colors[i%5]} relative p-2'):
            #retreive data for each card
            dep_line = vvo_data.get_data_entry(dep_data, i, 'LineName')
            dep_dir =  vvo_data.get_data_entry(dep_data, i, 'Direction')
            dep_time_sched =  vvo_data.get_data_entry(dep_data, i, 'ScheduledTime')
            dep_time_real =  vvo_data.get_data_entry(dep_data, i, 'RealTime')
            dep_state =  vvo_data.get_data_entry(dep_data, i, 'State')

            #process time
            dep_time_sched = vvo_data.convert_dotnet_date(dep_time_sched)
            dep_time_real = vvo_data.convert_dotnet_date(dep_time_real)
            dep_time_delta = vvo_data.get_time_delta(dep_time_real)
            dep_time_delta = vvo_data.format_deltatime_for_display(dep_time_delta)
            dep_time_real = vvo_data.format_time_for_display(dep_time_real)
            dep_time_sched = vvo_data.format_time_for_display(dep_time_sched)

            # Top-left label
            ui.label(dep_line + ' ' + dep_dir).classes('absolute top-2 left-2  text-lg  font-bold')
            # Top-right label
            ui.label(str(dep_time_delta)).classes('absolute top-2 right-2  text-lg font-bold')
            # Bottom-left label
            ui.label(dep_state).classes('absolute bottom-2 left-2  text-lg font-bold')
            # Bottom-right label
            ui.label(str(dep_time_real)).classes('absolute bottom-2 right-2  text-lg font-bold')
            #.strftime('%I:%M')
ui.run()


