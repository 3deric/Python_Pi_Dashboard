from nicegui import Client, ui
from datetime import datetime


@ui.page('/')
def page(client : Client):
    client.content.classes('p-0')

    ui.add_css('''
    .q-tabs,
    .q-tab-panels,
    .q-tab-panel {
        background: transparent !important;
    }
    ''')

    with ui.grid(columns= 2).classes('w-[800px] h-[480px] bg-green gap-0 p-0').style('grid-template-columns: auto auto auto auto'):

        with ui.column().classes(f'w-[300px] h-full relative gap-1'):
            ui.label('Time').classes('absolute top-1 right-1 font-bold')

        with ui.column().classes(f'w-[500px] h-full relative gap-1'):
            # right panel
            with ui.tabs().classes('w-full') as tabs:
                ui.tab('tab_transport', label = '', icon = 'o_directions_bus')
                ui.tab('tab_weather', label = '', icon = 'o_cloud')
                ui.tab('tab_calendar', label = '', icon = 'o_calendar_month')
            with ui.tab_panels(tabs, value = 'tab_transport').classes('w-full h-full'):
                with ui.tab_panel('tab_transport').classes('w-full h-full gap-1 p-1'):
                    for i in range(7):
                        with ui.card().classes(f'w-full h-full'):
                            ui.label('Line and Dir').classes('absolute top-1 left-2 font-bold')
                            # Top-right label
                            ui.label('Delta Time').classes('absolute top-1 right-2 font-bold')
                            # Bottom-left label
                            ui.label('State').classes('absolute bottom-1 left-2 font-regular')
                            # Bottom-right label
                            ui.label('Real Time').classes('absolute bottom-1 right-2 font-regular')
                with ui.tab_panel('tab_weather').classes('w-full h-full gap-0'):
                    pass

                with ui.tab_panel('tab_calendar').classes('w-full h-full gap-0 p-0'):
                    pass


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()