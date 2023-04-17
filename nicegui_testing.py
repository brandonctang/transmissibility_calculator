#!/usr/bin/env python3
from typing import Dict

from nicegui import ui
import numpy as np

ui.label('Well Penetration Direction')
penetration_direction = ui.radio(['i', 'j', 'k'], value='k').props('inline')

x_permeability = ui.number(label='Permeability X', value=0.001, )
y_permeability = ui.number(label='Permeability Y', value=0.001, )
z_permeability = ui.number(label='Permeability Z', value=0.0001, )

x_dimension = ui.number(label='X Dimension', value=100, )
y_dimension = ui.number(label='Y Dimension', value=100, )
z_dimension = ui.number(label='Z Dimension', value=10, )

wellbore_radius = ui.number(label='Wellbore Radius', value=0.3125, )
skin = ui.number(label='Skin', value=0, )

calculate_button = ui.button('Calculate!',
                             on_click=lambda: update_table_and_calculate_transmissibility(penetration_direction.value,
                                                                                          x_dimension.value,
                                                                                          y_dimension.value,
                                                                                          z_dimension.value,
                                                                                          x_permeability.value,
                                                                                          y_permeability.value,
                                                                                          z_permeability.value,
                                                                                          wellbore_radius.value,
                                                                                          skin.value))

grid = ui.aggrid({
    'columnDefs': [
        {'resizable':True, 'sortable':True, 'headerName': '#', 'field': 'index'},
        {'resizable':True, 'sortable':True, 'headerName': 'Penetration Direction', 'field': 'penetration_direction'},
        {'resizable':True, 'sortable':True, 'headerName': 'Perm X', 'field': 'permx'},
        {'resizable':True, 'sortable':True, 'headerName': 'Perm Y', 'field': 'permy'},
        {'resizable':True, 'sortable':True, 'headerName': 'Perm Z', 'field': 'permz'},
        {'resizable':True, 'sortable':True, 'headerName': 'X Dimension', 'field': 'dimx'},
        {'resizable':True, 'sortable':True, 'headerName': 'Y Dimension', 'field': 'dimy'},
        {'resizable':True, 'sortable':True, 'headerName': 'Z Dimension', 'field': 'dimz'},
        {'resizable':True, 'sortable':True, 'headerName': 'Wellbore Radius', 'field': 'wellbore_radius'},
        {'resizable':True, 'sortable':True, 'headerName': 'Skin', 'field': 'skin'},
        {'resizable':True, 'sortable':True, 'headerName': 'Transmissibility', 'field': 'transmissibility'}
    ],
    'rowData': [
    ],
    'rowSelection': 'multiple',
}).classes('max-h-1000')
grid.options['sortable'] = True
# grid.options['height'] = '100%'
# grid.options['width'] = '50%'
ui.button(text='clear', on_click=lambda: clear())


# ui.button(text='clear', on_click=lambda: grid.call_api_method('undoCellEditing'))


# grid.call_api_method("setWidthAndHeight('60%')")
def update_table(penetration_direction, x_dimension, y_dimension, z_dimension, x_permeability,
                 y_permeability, z_permeability, wellbore_radius, skin, transmissibility):

    grid.options['rowData'].append({
        'index':len(grid.options['rowData'])+1,
        'penetration_direction': penetration_direction,
        'permx': x_permeability,
        'permy': y_permeability,
        'permz': z_permeability,
        'dimx': x_dimension,
        'dimy': y_dimension,
        'dimz': z_dimension,
        'wellbore_radius': wellbore_radius,
        'skin': skin,
        'transmissibility': transmissibility
    })
    print(transmissibility)
    grid.update()


def clear():
    grid.options['rowData'] = []
    grid.update()


def calculate_transmissibility(penetration_direction, x_dimension, y_dimension, z_dimension, x_permeability,
                               y_permeability, z_permeability, wellbore_radius, skin):
    conversion = 0.001127
    if penetration_direction == 'i':
        equivalent_radius = 0.28 * (z_dimension ** 2 * (y_permeability / z_permeability) ** 0.5 + y_dimension ** 2 * (
                z_permeability / y_permeability) ** 0.5) ** 0.5 / ((y_permeability / z_permeability) ** 0.25 + (
                z_permeability / y_permeability) ** 0.25)
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
    return transmissibility


def update_table_and_calculate_transmissibility(penetration_direction, x_dimension, y_dimension, z_dimension,
                                                x_permeability,
                                                y_permeability, z_permeability, wellbore_radius, skin):
    transmissibility = calculate_transmissibility(penetration_direction, x_dimension, y_dimension, z_dimension,
                                                  x_permeability,
                                                  y_permeability, z_permeability, wellbore_radius, skin)
    update_table(penetration_direction, x_dimension, y_dimension, z_dimension, x_permeability,
                 y_permeability, z_permeability, wellbore_radius, skin, transmissibility)
    return transmissibility


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


ui.run(host='127.0.0.1', port=8081)
