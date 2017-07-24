import config
import utils
import socket
import re
from _thread import start_new_thread
import db
from time import sleep


def main():
    s = socket.socket() #установка соединения
    utils.connection(s) #-//-
    print(s)

#    utils.mess(s, "Hello") #первоначальное приветствие

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    start_new_thread(utils.fillOpList, ()) #проверка списка присутствующих модераторов
#    start_new_thread(utils.info, (s, 600)) #спам инфой

    while True: #пропуск "интро" твича
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True: #основное тело. здесь бот получает сообщения из чата и посылает по функциям для обработки
        response = s.recv(1024).decode() #получение пакета с сообщением
#        print(response)
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode())
            print("PONG SENT")
        else:
            username = re.search(r"\w+", response).group(0) #определение никнейма
            message = chat_message.sub("", response) #определение самого сообщения
            message = message.strip() #обработка сообщения
            print('MSG### ' + username + ': ' + message) #вывод сообщения в лог(консоль)
            if len(message) > 3:
                isitdone = db.addPoint(username, 1) #добавление очков юзеру, в сообщении которого больше трех символов
            utils.isCommand(s, username, message) #проверка на наличие в сообщении какой-нибудь команды


if __name__ == "__main__":
    main()

#########################сделать что-то, зависимое от дня первого сообщения/фоллова/подписки