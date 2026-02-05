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

    with ui.grid(columns = 2, rows = 1).classes('w-[800px] h-[480px] bg-grey gap-2 p-2').style('grid-template-columns: 1fr 2fr'):

        with ui.column().classes('w-full h-full relative gap-2 p-0'):
            with ui.card().classes('w-full h-50 gap-2 p-2'):
                with ui.column(wrap = False, align_items = 'center').classes('w-full h-full gap-2 p-2'):
                    ui.label(datetime.now().strftime('%H:%M')).style('font-size: 600%; font-weight: 600; line-height: 1')
                    ui.label(datetime.now().strftime('%A, %D')).style('font-size: 150%; font-weight: 300; line-height: 0.5')
            with ui.card().classes('w-full h-full gap-0 p-0'):
                ui.label('Weather').classes('font-bold')

        with ui.column().classes('w-full h-full relative gap-0 p-0'):
            # right panel
            with ui.card().classes('w-full h-full gap-0 p-0'):
                with ui.tabs().classes('w-full') as tabs:
                    ui.tab('tab_transport', label = '', icon = 'o_directions_bus')
                    ui.tab('tab_weather', label = '', icon = 'o_cloud')
                    ui.tab('tab_calendar', label = '', icon = 'o_calendar_month')
                with ui.tab_panels(tabs, value = 'tab_transport').classes('w-full h-full'):
                    #tab panel transport
                    with ui.tab_panel('tab_transport').classes('gap-0 p-0 w-full h-full gap-0 p-0'):
                        with ui.list().props('dense separator').classes('w-full h-full'):
                            for i in range(10):
                                with ui.item():
                                    with ui.item_section().props('middle_panel'):
                                        ui.label('Line and Dir').classes('font-bold')
                                        ui.label('State').classes('font-regular')
                                    with ui.item_section().props('right_panel'):
                                        ui.label('Delta Time').classes('text-right font-bold')
                                        ui.label('Real Time').classes('text-right font-regular')
                    #tab panel weather
                    with ui.tab_panel('tab_weather').classes('w-full h-full gap-0'):
                        pass

                    #tab panel calendar
                    with ui.tab_panel('tab_calendar').classes('w-full h-full gap-0 p-0'):
                        pass


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()