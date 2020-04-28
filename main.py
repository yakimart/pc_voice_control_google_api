import pyttsx3, speech_recognition as sr
import keyboard
import os, sys
import pyautogui
import datetime
from playsound import playsound
import json

with open('config.json', encoding="utf-8") as x:
    config = json.load(x)
    user_programs = list(config['user_programs'].keys())
    scroll_length = config["scroll_length"]
    greetings = config["greetings"]
    debugging_mode = config["debugging_mode"]


def open_app(voice):
    if 'документы' in voice:
        os.system(r"explorer.exe c:\\Documents")
        speak('Папка документы')
    elif 'проводник' in voice:
        os.system(r"explorer.exe C:\\")
        speak('Проводник запущен')
    elif 'браузер' in voice:
        os.system(r"explorer.exe C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        speak('Браузер запущен')
    elif 'загрузки' in voice:
        os.system(r"explorer.exe c:\\Downloads")
        speak('Папка с загрузками')
    elif 'изображения' in voice:
        os.system(r"explorer.exe c:\\Pictures")
        speak('Папка изображений')
    elif any(x in voice for x in user_programs):
        prog = list(set(voice) & set(user_programs))
        os.system(r"explorer.exe " + str(config['user_programs'][prog[0]]))
        speak('Запущен ' + str(prog[0]))
    elif 'список программ' or 'мои программы' in voice:
        speak('Ваши программы: ')
        speak(user_programs)


def scroll():
    speak('Включен режим прокрутки')
    while True:
        audio = r.listen(source)
        result = r.recognize_google(audio, language="ru-RU")
        print(result)
        if any(x in result for x in ['вниз', 'ниже']):
            pyautogui.scroll(-scroll_length)
        elif any(x in result for x in ['вверх', 'выше']):
            pyautogui.scroll(scroll_length)
        elif any(x in result for x in ['стоп', 'завершить', 'отмена', 'отменить']):
            speak('режим прокрутки выключен')
            return False
        else:
            continue

def voice_print():
    speak('Включен режим голосового набора')
    while True:
        audio = r.listen(source)
        result = r.recognize_google(audio, language="ru-RU")
        keyboard.write(result + ' ')
        if any(x in result for x in ['стоп', 'завершить', 'отмена', 'отменить']):
            speak('режим голосового набора выключен')
            return False


def calc(voice):
    voice[0] = ""
    while True:
        if ('умножить' in voice):
            voice[voice.index('умножить')] = '*'
        elif ('x' in voice):
            voice[voice.index('поделить')] = '*'
        elif ('поделить' in voice):
            voice[voice.index('поделить')] = '/'
        elif ('плюс' in voice):
            voice[voice.index('плюс')] = '+'
        elif ('минус' in voice):
            voice[voice.index('минус')] = '-'
        elif ('на' in voice):
            voice[voice.index('на')] = ''
        else: break

    a = eval(''.join(voice))
    speak('Ответ: ' + str(a))

def speak_time():
    t = datetime.datetime.now()
    a1, a2 = '', ''
    if t.hour in (2, 3, 4, 22, 23):
        a1 = ' часа '
    elif t.hour in (1, 21):
        a1 = ' час '
    else:
        a1 = ' часов '

    if t.minute in (1, 21, 31, 41, 51):
        a2 = ' минута '
    else:
        a2 = ' минут '

    speak(str(t.hour) + a1 + str(t.minute) + a2)

def execute(voice):
    if debugging_mode: print('execution')
    alert_sound(0)
    voice = voice.lower().split()
    if voice[0] in ('запустить', 'открыть'):
        open_app(voice)
    elif voice[0] in ('закрыть'):
        keyboard.press_and_release('alt + f4')
        speak('Окно закрыто')
    elif any(x in voice for x in ['прокрутка', 'прокрутки', 'скроллинг', 'скроллинга', 'скролл']):
        scroll()
    elif any(x in voice for x in ['диктовка', 'диктовку', 'набор', 'текст', 'текста']):
        voice_print()
    elif any(x in voice for x in ['время', 'час']):
        speak_time()
    elif any(x in voice for x in ['стоп', 'завершить', 'отмена', 'отменить']):
        speak('До новых встреч')
        sys.exit(0)
    elif voice == ['завершить', 'работу']:
        speak('Выключаю компьютер. До свидания')
    elif voice[0] in ('посчитай', 'посчитать', 'вычисли', ['сколько', 'будет']):
        calc(voice)
    else: speak('Ваш запрос не может быть выполнен')

def speak(what):
    speak_engine = pyttsx3.init()
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def alert_sound(arg):
    sound = ['success.wav', 'wait.wav']
    try: playsound(sound[arg])
    except:
        if arg == 1:
            speak('Я вас слушаю')
        else: pass

def recognize(source):
    alert_sound(1)
    try:
        audio = r.listen(source)
        if debugging_mode: print('got audio')
        result = r.recognize_google(audio, language="ru-RU")
        if debugging_mode: print('got recognized')
        if debugging_mode: print(result)
        execute(result)
    except:
        speak('Ваша речь не внятна, повторите пожалуйста')
        recognize(source)


with sr.Microphone(device_index=1) as source:
    speak(greetings)
    r = sr.Recognizer()
    r.energy_threshold = 120
    keyboard.add_hotkey('ctrl+alt', recognize, args=[source])
    keyboard.wait('esc')










