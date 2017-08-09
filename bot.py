import datetime
import re
import socket
from _thread import start_new_thread

import config
import db
import utils

infobool = False

def main():
    s = socket.socket()  # установка соединения
    utils.connection(s)  # -//-
    print(s)
    file = open('log.txt', 'a') # запись в лог даты текущего запуска
    file.write('\n\n' + datetime.datetime.now().strftime('%d:%m:%Y-[%I h:%M m: %S s]') + '\n')
    file.close()

    #    utils.mess(s, "Hello") #первоначальное приветствие

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    start_new_thread(utils.fillOpList, ())  # проверка списка присутствующих модераторов
    #    start_new_thread(utils.info, (s, 600)) #спам инфой

    while True:  # пропуск "интро" твича
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:  # основное тело. здесь бот получает сообщения из чата и посылает по функциям для обработки
        try:
            response = s.recv(1024).decode()  # получение пакета с сообщением
#            print(response)
        except Exception:
            print('smth wrong happened')
        if response == "PING :tmi.twitch.tv\r\n": # отвечает на проверку пингом, чтобы не кикнуло с сервера
            s.send("PONG :tmi.twitch.tv\r\n".encode())
            print("PONG SENT")
        else:
            try:
                username = re.search(r"\w+", response).group(0)  # определение никнейма
                message = chat_message.sub("", response)  # определение самого сообщения
                message = message.strip()  # обработка сообщения
                with open('log.txt', 'a') as f:
                    f.write('MSG### ' + username + ': ' + message + '\n')
                print('MSG### ' + username + ': ' + message)  # вывод сообщения в лог(консоль)

                utils.isCommand(s, username, message)  # проверка на наличие в сообщении какой-нибудь команды
            except Exception as msg: # ловит ошибки и записывает их в лог для дальнейшего дебага
                print('#ERROR:', msg)
                with open('log.txt', 'a') as f:
                    f.write('#ERROR: ' + str(msg) + '\n')


if __name__ == "__main__":
    main()
