#%%
# Package calls
# these are native packages
from urllib.request import urlopen, Request
from io import BytesIO

# pip installs required for these
import PySimpleGUI as sg
from PIL import Image, UnidentifiedImageError
# import requests

def resize(image_file, new_size, encode_format='PNG'):
    im = Image.open(image_file)
    new_im = im.resize(new_size, Image.NEAREST)
    with BytesIO() as buffer:
        new_im.save(buffer, format=encode_format)
        data = buffer.getvalue()
    return data

#%%
# Defining settings

track_title = 'Ironmon Tracker'
track_size = (300, 600)
sg.set_options(font=('Franklin Gothic Medium', 16), text_color='white', background_color='black', element_background_color='black', text_element_background_color='black')

#%% 
# Building the file
topcol1 = [
    [sg.Text('Slot 1', size=(20,1)),],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\gen6models\Porygon-Z.png', (120,120)))], 
    [sg.Text('Porygon-Z', justification='c'), sg.Text('#474', font=('Arial', 11, 'bold'))],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\types\Normal.png', (18, 16))), sg.Text('Normal', text_color='#999999')],
    [sg.Text('Level: '), sg.Text('25', tooltip='Seen at [8,9]')],
    [sg.Text('Speed Boost')],
    [sg.Text('@None')],
]

topcol2 = [
    [sg.Text('HP:')],
    [sg.Text('Atk:')],
    [sg.Text('Def:')],
    [sg.Text('SpAtk:')],
    [sg.Text('SpDef:')],
    [sg.Text('Speed:')],
    [sg.Text('BST:')],
]

topcol3 = [
    [sg.Text('91/91')],
    [sg.Text('46')],
    [sg.Text('69')],
    [sg.Text('32')],
    [sg.Text('66')],
    [sg.Text('52')],
    [sg.Text('535')],
]

botcol1 = [
    [sg.Text('Moves 4/12 (29)')],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\categories\Physical.png', (27,20))), sg.Text('Gear Grind')],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\categories\Physical.png', (27,20))), sg.Text('Flamethrower')],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\categories\Special.png', (27,20))), sg.Text('Horn Attack')],
    [sg.Image(resize(r'D:\Games\Pokemon\Citra\nightly\scripting\images\categories\Physical.png', (27,20))), sg.Text('Knock Off')],
]

botcol2 = [
    [sg.Text('PP')],
    [sg.Text('15/15')],
    [sg.Text('15/15')],
    [sg.Text('25/25')],
    [sg.Text('20/20')],
]

botcol3 = [
    [sg.Text('BP')],
    [sg.Text('50')],
    [sg.Text('90')],
    [sg.Text('65*')],
    [sg.Text('65')],
]

botcol4 = [
    [sg.Text('Acc')],
    [sg.Text('85')],
    [sg.Text('100')],
    [sg.Text('100')],
    [sg.Text('100')],
]

botcol5 = [
    [sg.Text('C')],
    [sg.Text('Y')],
    [sg.Text('N')],
    [sg.Text('Y')],
    [sg.Text('Y')],
]

layout = [
    [
        [
            sg.Column(topcol1, element_justification='bottom'),
            sg.Column(topcol2),
            sg.Column(topcol3, element_justification='right'),
        ], 
        [
            sg.Column(botcol1),
            sg.Column(botcol2, element_justification='right'),
            sg.Column(botcol3, element_justification='right'),
            sg.Column(botcol4, element_justification='right'),
            sg.Column(botcol5, element_justification='right'),
        ]
    ]
]



# layout = [[sg.Text('Testing Python UIs')], [sg.Button('OK')]]

window = sg.Window(track_title, layout, track_size, background_color='black')

while True:
    event, values = window.read()
    if event == 'OK' or event == sg.WIN_CLOSED:
        break