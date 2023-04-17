#!/usr/bin/env python3
from typing import Dict

from nicegui import ui

ui.label('Well Penetration Direction')
penetration_direction = ui.radio(['i', 'j', 'k'], value='k').props('inline')

x_permeability = ui.number(label='Permeability X', value=100, )
y_permeability = ui.number(label='Permeability Y', value=100, )
z_permeability = ui.number(label='Permeability Z', value=10, )

x_dimension = ui.number(label='X Dimension', value=100, )
y_dimension = ui.number(label='Y Dimension', value=100, )
z_dimension = ui.number(label='Z Dimension', value=10, )

wellbore_radius = ui.number(label='Wellbore Radius', value=0.3125, )
skin = ui.number(label='Skin', value=0, )

calculate_button = ui.button('Calculate!', on_click=lambda: result.set_text(wellbore_radius.value))

result = ui.label()


def calculate_transmissibility(penetration_direction, x_dimension, y_dimension, z_dimension, x_permeability,
                               y_permeability, z_permeability, wellbore_radius, skin):
    conversion = 0.001127
    if penetration_direction == 'i':
        equivalent_radius = 0.28 * (z_dimension ** 2 * (y_permeability / z_permeability) ** 0.5 + y_dimension ** 2 * (
                x_permeability / y_permeability) ** 0.5) ** 0.5 / ((y_permeability / z_permeability) ** 0.25 + (
                x_permeability / y_permeability) ** 0.25)
        transmissibility = conversion * 2 * np.pi * x_permeability * x_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)
    elif penetration_direction == 'j':
        equivalent_radius = 0.28 * (x_dimension ** 2 * (z_permeability / x_permeability) ** 0.5 + z_dimension ** 2 * (
                x_permeability / z_permeability) ** 0.5) ** 0.5 / ((z_permeability / x_permeability) ** 0.25 + (
                x_permeability / z_permeability) ** 0.25)
        transmissibility = conversion * 2 * np.pi * y_permeability * y_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)
    elif penetration_direction == 'k':
        equivalent_radius = 0.28 * (x_dimension ** 2 * (y_permeability / x_permeability) ** 0.5 + y_dimension ** 2 * (
                x_permeability / y_permeability) ** 0.5) ** 0.5 / ((y_permeability / x_permeability) ** 0.25 + (
                x_permeability / y_permeability) ** 0.25)
        transmissibility = conversion * 2 * np.pi * z_permeability * z_dimension / (
                np.log(equivalent_radius / wellbore_radius) + skin)


#
# tab_names = ['A', 'B', 'C']
#
# # necessary until we improve native support for tabs (https://github.com/zauberzeug/nicegui/issues/251)
#
#
# def switch_tab(msg: Dict) -> None:
#     name = msg['args']
#     tabs.props(f'model-value={name}')
#     panels.props(f'model-value={name}')
#
#
# with ui.header().classes(replace='row items-center') as header:
#     ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')
#     with ui.element('q-tabs').on('update:model-value', switch_tab) as tabs:
#         for name in tab_names:
#             ui.element('q-tab').props(f'name={name} label={name}')
#
# with ui.footer(value=False) as footer:
#     ui.label('Footer')
#
# with ui.left_drawer().classes('bg-blue-100') as left_drawer:
#     ui.label('Side menu')
#
# with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
#     ui.button(on_click=footer.toggle).props('fab icon=contact_support')
#
#
# # the page content consists of multiple tab panels
# with ui.element('q-tab-panels').props('model-value=A animated').classes('w-full') as panels:
#     for name in tab_names:
#         with ui.element('q-tab-panel').props(f'name={name}').classes('w-full'):
#             ui.label(f'Content of {name}')
#
#             grid = ui.aggrid({
#                 'columnDefs': [
#                     {'headerName': 'Name', 'field': 'name'},
#                     {'headerName': 'Age', 'field': 'age'},
#                 ],
#                 'rowData': [
#                     {'name': 'Alice', 'age': 18},
#                     {'name': 'Bob', 'age': 21},
#                     {'name': 'Carol', 'age': 42},
#                 ],
#                 'rowSelection': 'multiple',
#             }).classes('max-h-40')
#
#
#             def update():
#                 grid.options['rowData'][0]['age'] += 1
#                 grid.update()
#
#
#             ui.button('Update', on_click=update)
#             ui.button('Select all', on_click=lambda: grid.call_api_method('selectAll'))
#


ui.run()
