import telebot
import iperf3
import matplotlib.pyplot as plt
import scipy


bot = telebot.TeleBot('your bot token')
wse = []
displayer = []
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Бажаю здоровля 🫡')



@bot.message_handler(commands=["play"])
def displaye(message):
    displaym = bot.send_message(message.from_user.id, 'Введiть формат вивода 1.Графік 2. Текст: ')
    bot.register_next_step_handler(displaym, timeplay)
    print(message.text)


def timeplay(message):
    displayer.append(message.text)
    timeplay = bot.send_message(message.from_user.id, 'Введiть час перевiрки: ')
    bot.register_next_step_handler(timeplay, itsip)
    print(message.text)


def itsip(message):
    wse.append(message.text)
    itsip = bot.send_message(message.from_user.id, 'Введiть ip перевiрки: ')
    bot.register_next_step_handler(itsip, handle_text)
    print(message.text)


def handle_text(message):
    itsip = message.text
    print('ip перевiрки: : ', itsip)
    print('Час перевiрки: ', int(wse[0]))
    client = iperf3.Client()
    client.duration = int(wse[0])
    client.server_hostname = itsip
    a = client.run()
    data = a.json
    wse.clear()
    byte = []
    time = []
    if int(displayer[0]) == 1:
        for i in data['intervals']:
            starts = round(int(i['streams'][0]['start']))
            end = round(int(i['streams'][0]['end']))
            brandwitch = round(int(i['streams'][0]['bits_per_second']) / 8e+6, 2)
            transfer = round(int(i['streams'][0]['bytes']) / 1e+6, 2)
            byte.append(transfer)
            time.append(starts)
        plt.plot(time, byte)
        plt.savefig("mygraph.png")
        photo = open('mygraph.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        displayer.clear()
    else:
        for i in data['intervals']:
            starts = round(int(i['streams'][0]['start']))
            end = round(int(i['streams'][0]['end']))
            brandwitch = round(int(i['streams'][0]['bits_per_second']) / 8e+6, 2)
            transfer = round(int(i['streams'][0]['bytes']) / 1e+6, 2)
            bot.send_message(message.chat.id, str(starts) + ' - ' + str(end) + 's' + ' | ' + str(transfer) + ' MB' +
                             ' | ' + str(brandwitch) + ' MB/s')


bot.polling(none_stop=True, interval=0)
