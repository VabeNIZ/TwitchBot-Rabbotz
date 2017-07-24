import time
import config
import urllib.request
import json
import db
import tts
from random import randint

from _thread import start_new_thread
from time import strftime, sleep


def connection(sock):
    sock.connect((config.HOST, config.PORT))
    sock.send("PASS {}\r\n".format(config.PASS).encode())
    sock.send("NICK {}\r\n".format(config.NICK).encode())
    sock.send("JOIN #{}\r\n".format(config.CHAN).encode())


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode())


def ban (sock, user):
    mess(sock, ".ban {}".format(user))


def timeout(sock, user, seconds = 600):
    mess(sock, ".timeout {}".format(user.seconds))


def fillOpList():
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
        except:
            print("Uhmmm...")
#        print(config.oplist)
        time.sleep(10)


def isOp(user):
    return user in config.oplist


def isCommand(sock, username, message):
    if message == "Кролик, время!":
        mess(sock, strftime("%I:%M %p on %A %B %d %Y"))
        sleep(1.5)
    elif message == 'Кролик, фас!':
        mess(sock, "Angery Angery Angery")
        sleep(1.5)
    elif message == 'Кто кролик?':
        mess(sock, "@" + username + " ты vovanK")
        sleep(1.5)
    elif message == 'Мой сад!':
        morkovka = db.countPoint(username)
        mess(sock, '@' + username + ' у тебя уже ' + str(morkovka[0]) + ' морковок :carrot: gachiGASM :carrot:')
        sleep(1.5)
    elif message[:16] == 'Кролик, прочти: ':
        readprice = 100
        if db.countPoint(username)[0] > readprice:
            start_new_thread(tts.tts, (message[16:],))
#            tts.tts(message[15:])
            db.takeawayPoint(username, readprice)#удаление очков
            mess(sock, '@' + username + ' списано ' + str(readprice) + ' морквы.')
                sleep(1.5)
        else:
            mess(sock, '@' + username + ' у вас недостаточно морковок.')
                sleep(1.5)
    elif message == 'Моя морковка!':
        size = db.createMSize(username)
        mess(sock, '@' + username + ' твоя морковка ' + str(size) + ' сантиметров.')
                sleep(1.5)
    elif message == 'Другая морковка!':
        mcount = db.countPoint(username)
        if int(mcount[0]) >= 50:
            size = db.setMSize(username, 0)
            mess(sock, '@' + username + ' теперь твоя морковка ' + str(size) + ' сантиметров.')
                sleep(1.5)
            db.takeawayPoint(username, 50)
        else:
            mess(sock, '@' + username + ' у тебя недостаточно морковок в саду, чтобы изменять размер своей собственной :(')
                sleep(1.5)
    elif message[:9] == 'Рулетка: ':
        roulettecount = message.split(' ')
        if str.isdecimal(roulettecount[1]):
            if int(roulettecount[1]) > 0:
                isitdone = db.takeawayPoint(username, roulettecount[1])
                if isitdone:
                    isroul = roulette(username, roulettecount[1])
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
                mess(sock, '@' + username + ' ты попытался считерить, фу-фу-фу panicBasket ')
                sleep(1.5)
        else:
            mess(sock, '@' + username + ' не ломай меня! SSSsss')
            sleep(1.5)
    elif username in config.oplist: ####### КОМАНДЫ ДЛЯ СТАФФА ############
        if message[:7] == '!mcount':
            mcount = db.countPoint(message[8:])
            if mcount is None:
                mess(sock, '@' + username + ' ошибка.')
                sleep(1.5)
            else:
                mess(sock, '@' + username + ' у ' + message[8:] + ' ' + str(mcount[0]) + ' морковок.')
                sleep(1.5)
        elif message[:6] == '!madd ':
            clist = message.split(' ')
            muser, mpoint = clist[1], clist[2]
            iid = db.addPoint(muser, mpoint)
            if iid is False:
                mess(sock, '@' + username + ' ошибка.')
                sleep(1.5)
            else:
                mess(sock, '@' + username + ' кролику ' + muser + ' добавлено ' + mpoint + ' морковок.')
                sleep(1.5)
        elif message[:8] == '!mtaway ':
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
        elif message[:11] == '!startinfo ':
            timee = message.split(' ')[1]
            infobool = True
            start_new_thread(info, (sock, timee, infobool)) #спам инфой
#        elif message == '!stopinfo':
#            infobool = False
#            start_new_thread(info, (sock, 600, infobool)) #спам инфой

def info(sock, time, infobool):
    while infobool:
        mess(sock,'Привет, я кролик-бот. Пока я мало чего умею, но вот ссылка на все мои доступные на данный момент команды - https://goo.gl/rY2pYm Angery')
        print('info1 sent')
        sleep(int(time))
        mess(sock,'За каждое ваше сообщение длиной от 4-х символов на ваш персональный сад начисляется морковка. Чтобы проверить количество морковок, выросших на вашем саду, введите "Мой сад!"')
        print('info2 sent')
        sleep(time)


def roulette(username, points):
    win = randint(0, 1)
    wpoint = int(points) * 2
    if win == 1:
        db.addPoint(username, int(wpoint))
        return True
    else:
        return False