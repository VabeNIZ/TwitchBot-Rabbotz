import json
import time
import urllib.request
from _thread import start_new_thread
from random import randint
from time import strftime, sleep

import config
import db
import tts
import bot


def connection(sock):
    sock.connect((config.HOST, config.PORT))
    sock.send("PASS {}\r\n".format(config.PASS).encode())
    sock.send("NICK {}\r\n".format(config.NICK).encode())
    sock.send("JOIN #{}\r\n".format(config.CHAN).encode())


def mess(sock, message): # функция отправки сообщений
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode())


def ban(sock, user): # функция бана усера
    mess(sock, ".ban {}".format(user))


def timeout(sock, user, seconds=600): # функция таймаута усера
    mess(sock, ".timeout {} {}".format(user, seconds))


def fillOpList(): # каждые десять секунд проверяет список текущих модераторов сервера и добавляет их в список
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/" + config.CHAN + "/chatters"
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            res = urllib.request.urlopen(req).read()
            if res.find("502 bad gateway".encode()) == -1:
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
        except Exception:
            print("Uhmmm...")
        # print(config.oplist)
        time.sleep(10)


def isOp(user): # возвращает True, если отправленный в эту функцию усер - модер
    return user in config.oplist


def isCommand(sock, username, message): # проверяет сообщение на наличие команд
    message = message.lower()
    if message[:8] == "кролик, ":
        if message == "кролик, время!":
            mess(sock, strftime("%I:%M %p on %A %B %d %Y"))
            sleep(1.5)
        elif message == 'кролик, фас!':
            mess(sock, "Angery Angery Angery")
            sleep(1.5)
        elif message[:16] == 'кролик, прочти: ':
            readprice = config.voiceprice
            if db.countPoint(username)[0] > readprice:
                if config.tts == 'yandex':
                    start_new_thread(tts.yandextts, (str(message[16:]),))
                else:
                    start_new_thread(tts.googletts, (str(message[16:]),))
                db.takeawayPoint(username, readprice)  # удаление очков
                mess(sock, '@' + username + ' списано ' + str(readprice) + ' морквы.')
                sleep(1.5)
            else:
                mess(sock, '@' + username + ' у вас недостаточно морковок.')
                sleep(1.5)
    elif message == 'кто кролик?':
        mess(sock, "@" + username + " ты vovanK")
        sleep(1.5)
    elif message == 'мой сад!':
        morkovka = db.countPoint(username)
        mess(sock, '@' + username + ' у тебя уже ' + str(morkovka[0]) + ' морковок :carrot: gachiGASM :carrot:')
        sleep(1.5)
    elif message == 'моя морковка!':
        size = db.createMSize(username)
        mess(sock, '@' + username + ' твоя морковка ' + str(size) + ' сантиметров.')
        sleep(1.5)
    elif message == 'другая морковка!':
        mcount = db.countPoint(username)
        if int(mcount[0]) >= 50:
            size = db.setMSize(username, 0)
            mess(sock, '@' + username + ' теперь твоя морковка ' + str(size) + ' сантиметров.')
            sleep(1.5)
            db.takeawayPoint(username, 50)
        else:
            mess(sock,
                 '@' + username + ' у тебя недостаточно морковок в саду, чтобы изменять размер своей собственной :(')
            sleep(1.5)
    elif message[:9] == 'рулетка: ':
        roulettecount = message.split(' ')
        if str.isdecimal(roulettecount[1]) and (int(roulettecount[1]) > 0):
            isitdone = db.takeawayPoint(username, roulettecount[1])
            if isitdone:
                isroul = roulette(username, roulettecount[1], sock)
                if isroul:
                    mess(sock, '@' + username + ' ты выиграл ' + roulettecount[1] + ' морковок Keepo')
                    sleep(1.5)
                else:
                    mess(sock, '@' + username + ' ты проиграл ' + roulettecount[1] + ' морковок panicBasket ')
                    sleep(1.5)
            else:
                mess(sock, '@' + username + ' в твоем саду нет столько морковок panicBasket ')
                sleep(1.5)
        else:
            mess(sock, '@' + username + ' не ломай меня! SSSsss')
            sleep(1.5)
    elif username in config.oplist:  ####### КОМАНДЫ ДЛЯ СТАФФА ############
        if message[:2] == "!m":
            if message[:7] == '!mcount':
                try:
                    mcount = db.countPoint(message[8:])
                    if mcount is None:
                        mess(sock, '@' + username + ' ошибка.')
                        sleep(1.5)
                    else:
                        mess(sock, '@' + username + ' у ' + message[8:] + ' ' + str(mcount[0]) + ' морковок.')
                        sleep(1.5)
                except Exception:
                    mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !mcount <user> ')
            elif message[:6] == '!madd ':
                try:
                    clist = message.split(' ')
                    muser, mpoint = clist[1], clist[2]
                    iid = db.addPoint(muser, mpoint)
                    if iid is False:
                        mess(sock, '@' + username + ' ошибка.')
                        sleep(1.5)
                    else:
                        mess(sock, '@' + username + ' кролику ' + muser + ' добавлено ' + mpoint + ' морковок.')
                        sleep(1.5)
                except Exception:
                    mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !madd <user> <amount> ')
            elif message[:8] == '!mtaway ':
                try:
                    clist = message.split(' ')
                    muser, mpoint = clist[1], clist[2]
                    iid = db.takeawayPoint(muser, mpoint)
                    if iid is False:
                        db.takeawayPoint(muser, db.countPoint(muser)[0])
                        mess(sock, '@' + username + ' ты отнял у ' + muser + ' все морковки')
                        sleep(1.5)
                    else:
                        mess(sock, '@' + username + ' ты отнял у ' + muser + ' ' + mpoint + ' морковок.')
                        sleep(1.5)
                except Exception:
                    mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !mtaway <user> <amount> ')
        elif message[:6] == "!info ":
            try:
                message = message.split(" ")
                if message[1] == 'start':   # спам инфой
                    timee = message[2]
                    bot.infobool = True
                    start_new_thread(info, (sock, timee))
                elif message[1] == 'stop':  # остановить спам инфой
                    bot.infobool = False
                    print('info stopped')
                else: mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !info [start/stop] <time>')
            except Exception:
                mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !info [start/stop] <time>')
        elif message == '!voices':
            mess(sock, '@' + username + ' Female: "jane", "oksana", "alyss", "omazh". Male: "zahar", "ermil"')
        elif message[:13] == '!changevoice ':
            message = message.split(' ')
            try:
                if message[1] in config.speakerlist:
                    config.speaker = message[1]
                    mess(sock, '@' + username + ' голос изменен на ' + message[1])
                else:
                    mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !changevoice <voice> . Female: "jane", "oksana", "alyss", "omazh". Male: "zahar", "ermil" ')
            except Exception:
                mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !changevoice <voice> . Female: "jane", "oksana", "alyss", "omazh". Male: "zahar", "ermil" ')
        elif message[:13] == '!changeprice ':
            try:
                message = message.split(' ')
                if message[1] == 'voice':
                    config.voiceprice = int(message[2])
                    mess(sock, '@' + username + ' цена озвучки была изменена на ' + message[1])
            except:
                mess(sock, '@' + username + ' что-то не то, попробуй еще раз - !changeprice [voice] <price> ')
    elif len(message) >= 3:
        db.addPoint(username, 1)


def info(sock, time): # функция спама инфой о боте
    while bot.infobool:
        mess(sock,
             'Привет, я кролик-бот. Пока я мало чего умею, но вот ссылка на все мои доступные на данный момент команды - https://goo.gl/rY2pYm Angery')
        print('info1 sent')
        sleep(int(time))
        if bot.infobool:
            mess(sock,
                 'За каждое ваше сообщение длиной от 4-х символов на ваш персональный сад начисляется морковка. Чтобы проверить количество морковок, выросших на вашем саду, введите "Мой сад!"')
            print('info2 sent')
            sleep(int(time))
    else:
        print('info stopped')


def roulette(username, points, sock): # рулетка
    win = randint(0, 1)
    wpoint = int(points) * 2
    if win == 1:
        db.addPoint(username, int(wpoint))
        return True
    else:
        return False


def info1(sock, time): # функция спама инфой о боте
    while 1:
        mess(sock,
             '░░░░░░░░░░░░░░░░░░░░░ ░░░▄█▀█▄█▀█▄▄▄░░░░░░░ ░░█▒░░▀█▄▄░░░▀▀█░░░░░ ░█▒░░░░░▒░░░░▒▄░▀▀█▄░ ░█▒░░░░█▒░░▄▀░░░▒░░█░ ░█▒░░░█▒░░█▀▒░░█▀░░▀█ ░█▒░░░█▒░░█▒░░█▓░░░▓█ ▄▀█▓▓░█▒░▓█▓░░█▓░░▓▄█ █▒▒████▄▓▓█▓░░█▓░░▄█░ █▒▒░░░░░▀█▄▀░▄▀▓▄█▀░░ █▒▓▓▓█▀▀▄▀█▄▄▀▄▄▀░░░░ ░▀▄▄▄█▄▄▀░░░░░░░░░░░░')
        print('info1 sent')
        sleep(int(time))
        if 1:
            mess(sock,
                 '░░░░░░░░░░░░░░░░░░░░ ░░░░░▄▀░░░░░░░░░░░░░ ░░░░█░▄██░░░░░░██▄░░ ░░░█▄▀▄▄░█░░░░█░▄░█▄ ░░▄▀░▀▀▀▀░░░░░░▀▀▀░░ ▄▀░░░░░░░░░░░░▄░░░░░ █░░░░█░░░░░░▄▄▀░░░░░ █░▄▀▄░▀▀▀▀▀▀░░░▄▀▀▄░ ▀▄▀░░▀▀▄▄▄▄▄(_̅_̅_̅_̅_̅_̅_̅_̅_̅_̅_̅_̅_̅_̅ () ด้็็็็็้็็็็็้็็็็็้็็็็็้็็็็็้็็็็็้็็็็็้็็็็็ . ░▀▄░░░░░░░░░░░░░░░░░ ░░█░░░░░░░░░░░░░░░░░')
            print('info2 sent')
            sleep(int(time))