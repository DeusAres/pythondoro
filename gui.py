import PySimpleGUI as sg
import settings
import image

def settingsWin():
    sets = settings.read()
    saved = False
    layout = [
        [
            [sg.Text('Pomodoro lenght', s=(20,1)), sg.Input(sets['pomodoro'], key='pomodoro')],
            [sg.Text('Pause lenght', s=(20,1)), sg.Input(sets['pause'], key='pause')],
            [sg.Checkbox('Auto start pomodoro', default=sets['autopomodoro'], s=(20,1), key='autopomodoro')],
            [sg.Checkbox('Auto start pause', default=sets['autopause'], s=(20,1), key='autopause')],
            [sg.Push(), sg.Text('Saving settings will reset the timer!'), sg.Push()],
            [sg.Push(), sg.Button('Save'), sg.Button('Discard')]
        ]
    ]
    window = sg.Window("Settings", layout)
    while True:
        event, values = window.read()

        if event in [sg.WINDOW_CLOSED, 'Discard', 'Save']:
            if event == 'Save':
                saved = True
                settings.set(values)
            break

    window.close()
    return saved

    
def noTop(moment='Productivity time', disabled=True):
    s = (6, 1)
    l = [
            [
                sg.Column([
                    [sg.Text(moment, key='inWhichMoment')],
                    [sg.Text('00:00:00', key='timer')],
                    [sg.Button('Start', s=s), sg.Button('Pause', disabled=disabled, s=s), sg.Button('Reset', s=s), sg.Button('On top', s=s)]
                ], element_justification='center')
            ]
        ]
    window = sg.Window('Pythondoro', l, icon=image.icon, right_click_menu=['', ['Settings']], finalize=True)
    return window

def onTop(moment='Productivity time'):
    l = [
            [
                sg.Column([
                    [sg.Text(moment, s=(14,1), key='inWhichMoment'), sg.Text('00:00:00', s=(8, 1), key='timer')],
                ], element_justification='center'),
            ]
        ]   
    window = sg.Window('Pythondoro', l, icon=image.icon, no_titlebar=True,
                                size=(200,30), 
                                margins=(0,0),
                                keep_on_top=True,
                                grab_anywhere=True,
                                right_click_menu=['', ['Enlarge']],
                                finalize = True, 
    )
    return window
