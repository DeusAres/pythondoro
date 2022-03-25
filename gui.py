import PySimpleGUI as sg
import settings

def settingsWin():
    sets = settings.read()
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
                settings.set(values)
            break

    window.close()

def noTop(moment='Productivity time', disabled=True):
    l = [
            [
                sg.Column([
                    [sg.Text(moment, key='inWhichMoment')],
                    [sg.Text('00:00:00', key='timer')],
                    [sg.Button('Start'), sg.Button('Pause', disabled=disabled), sg.Button('Reset'), sg.Button('On top')]
                ], element_justification='center')
            ]
        ]

    window = sg.Window('Yet another pomodoro', l, right_click_menu=['', ['Settings']], finalize=True)
    return window

def onTop(moment='Productivity time'):
    l = [
            [
                sg.Column([
                    [sg.Text(moment, key='inWhichMoment')],
                    [sg.Text('00:00:00', key='timer')],
                ], element_justification='center'),
            ]
        ]   
    window = sg.Window('', l,   no_titlebar=True,
                                auto_size_buttons=False,
                                keep_on_top=True,
                                grab_anywhere=True,
                                right_click_menu=['', ['Enlarge']],
                                finalize = True, 
    )
    return window
