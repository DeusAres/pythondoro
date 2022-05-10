import PySimpleGUI as sg
import settings
from playsound import playsound
from threading import Thread
from pathlib import Path
import gui
import traceback
import os
from win10toast import ToastNotifier

os.chdir(Path(__file__).parents[0])

def main():
    sg.LOOK_AND_FEEL_TABLE["DarkPoker"] = {
        "BACKGROUND": "#252525",
        "TEXT": "#FFFFFF",
        "INPUT": "#af0404",
        "TEXT_INPUT": "#FFFFFF",
        "SCROLL": "#af0404",
        "BUTTON": ("#FFFFFF", "#252525"),
        "BORDER": 1,
        "SLIDER_DEPTH": 0,
        "PROGRESS_DEPTH": 0,
        "COLOR_LIST": ["#252525", "#414141", "#af0404", "#ff0000"],
        "PROGRESS": ("# D1826B", "# CC8019"),
    }
    sg.theme("DarkPoker")

    try:
        sets = settings.read()
    except:
        settings.first()
        sets = settings.read()

    window = gui.noTop()

    def updateTimer():
        window['timer'].Update('{:02d}:{:02d}.{:02d}'.format(secondsToElapse // 3600, secondsToElapse // 60, secondsToElapse % 60))

    def play():
        try:
            if getMoment() == 'Productivity time':
                ToastNotifier().show_toast(
                    "Productivity time",
                    "Time to work hard!",
                    duration=10,
                    icon_path="icon.ico",
                    threaded=True
                )
                playsound('./sounds/pomodoro.mp3')
            elif getMoment() == 'Break time':
                ToastNotifier().show_toast(
                    "Break time",
                    "Chill for a bit, you deserve it",
                    duration=10,
                    icon_path="icon.ico",
                    threaded=True
                )
                playsound('./sounds/pause.mp3')
        except:
            print(traceback.format_exc())

    def getMoment():
        return window['inWhichMoment'].DisplayText

    secondsToElapse = sets['pomodoro'] * 60
    clockRunning = False
    updateTimer()

    while True:
        event, values = window.read(1000)

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Start':
            if getMoment() == 'Productivity time':
                secondsToElapse = sets['pomodoro'] * 60
            elif getMoment() == 'Break time':
                secondsToElapse = sets['pause'] * 60
            clockRunning = True
            window['Pause'].Update(disabled=False)

        if event == 'Pause' and window['Pause'].ButtonText == 'Pause':
            clockRunning = False
            window['Pause'].Update('Resume')
        elif event == 'Pause' and window['Pause'].ButtonText == 'Resume':
            clockRunning = True
            window['Pause'].Update('Pause')

        if event == 'Reset':
            secondsToElapse = sets['pomodoro'] * 60
            window['inWhichMoment'].Update('Productivity time')
            updateTimer()
            clockRunning = False


        if event in ['On top', 'Enlarge']:
            window.close()
            if event == 'On top': window = gui.onTop(getMoment())
            if event == 'Enlarge': window = gui.noTop(getMoment(), not clockRunning)


        if secondsToElapse == 0 and clockRunning == True:
            first = ['Productivity time', 'autopause', 'pause']
            second = ['Break time', 'autopomodoro', 'pomodoro']

            def firstSecond(a, b, secondsToElapse, clockRunning):
                if getMoment() == a[0]:
                    window['inWhichMoment'].Update(b[0])
                    Thread(target=play).start()
                    secondsToElapse = sets[a[2]] * 60
                    if not sets[a[1]]:
                        clockRunning = False
                        #window['Pause'].Update(disabled=True)

                    return secondsToElapse, clockRunning
                return False

            result = firstSecond(first, second, secondsToElapse, clockRunning)
            if not result:
                result = firstSecond(second, first, secondsToElapse, clockRunning)
            if result:
                secondsToElapse, clockRunning = result
            """
            if getMoment() == 'Productivity time':
                window['inWhichMoment'].Update('Break time')
                Thread(target=play).start()
                if sets['autopause']:
                    secondsToElapse = sets['pause'] * 60
                else:
                    clockRunning = False
                    window['Pause'].Update(disabled=True)
                    
            elif getMoment() == 'Break time':
                window['inWhichMoment'].Update('Productivity time')
                Thread(target=play).start()
                if sets['autopomodoro']:
                    secondsToElapse = sets['pomodoro'] * 60
                else:
                    clockRunning = False
                    window['Pause'].Update(disabled=True)
            """
        if clockRunning:
            secondsToElapse -= 1
        
        if event == 'Settings':
            window.close()
            saved = gui.settingsWin()
            window = gui.noTop(getMoment(), not clockRunning)
            if saved:
                sets = settings.read()
                secondsToElapse = sets['pomodoro'] * 60
                updateTimer()
                window['inWhichMoment'].Update('Productivity time')
                clockRunning = False

        updateTimer()
                
    window.close()


if __name__ == '__main__':
    import traceback
    from pyperclip import copy
    try:
        main()
    except:
        sg.Popup(traceback.format_exc()+'\n'+'Hit ok to copy the error to clipboard'+'\n'+'Report it on https://github.com/DeusAres/Pythondoro/issues please!', title='Bug!')
        copy(traceback.format_exc())
