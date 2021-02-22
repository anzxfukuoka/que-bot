import sys
import os
import telebot
from flask import Flask, request

token = "1638080970:AAFfULuQr1san3QxUoPEoQv4VSHBORyOdXY"

bot = telebot.TeleBot(token)

server = Flask(__name__)

"""
def load_queue():
    with open("data.q", "a+", encoding="utf-8") as f:
        data = f.read()
        queue = data.split("\n")
        queue = [q for q in queue if q != ""]
    return queue

def save_queue(queue):
    with open("data.q", "w+", encoding="utf-8") as f:
        data = "\n".join([q for q in queue if q != ""])
        f.write(data)
"""

queue = []

print(load_queue())

help = """
/start - перезагрузить бота
/help - список команд
/clear - очистить очередь
/push - встать в очередь
/pop - выйти из очереди
/next - некст
/show - вывести очередь
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, help)
    print("new user: " + message.from_user.username)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, help)


@bot.message_handler(commands=['clear'])
def send_clear(message):
    #save_queue([])
    global queue
    queue = []
    bot.send_message(message.chat.id, "очередь очищенна")


@bot.message_handler(commands=['push'])
def send_push(message):

    #queue = load_queue()

    if message.from_user.username not in queue:
        queue.append(message.from_user.username)
        bot.send_message(message.chat.id, message.from_user.username + " встал в конец очереди")
    else:
        bot.send_message(message.chat.id, "ты уже в очереди")

    #save_queue(queue)


@bot.message_handler(commands=['pop'])
def send_pop(message):
    #queue = load_queue()

    if message.from_user.username not in queue:
        queue.pop(queue.index(message.from_user.username))
        bot.send_message(message.chat.id, message.from_user.username + " вышел из очереди")
    else:
        bot.send_message(message.chat.id, "ты не в очереди")

    #save_queue(queue)


@bot.message_handler(commands=['next'])
def send_next(message):
    #queue = load_queue()

    if len(queue) > 1:
        queue.pop(0)
        bot.send_message(message.chat.id, "@" + queue[0])
    elif len(queue) == 1:
        queue.pop(0)
        bot.send_message(message.chat.id, "дальше в очереди никого нет")
    else:
        bot.send_message(message.chat.id, "в очереди никого нет")

    #save_queue(queue)


@bot.message_handler(commands=['show'])
def send_show(message):
    #queue = load_queue()

    if len(queue) > 0:
        bot.send_message(message.chat.id, "очередь:\n" + "\n".join(queue))
    else:
        bot.send_message(message.chat.id, "в очереди никого нет")


@bot.message_handler(commands=['roll'])
def send_roll(message):
    re = bot.send_dice(message.chat.id)
    print(re.dice)


@bot.message_handler(func=lambda message: True)
def echo(message):
    #txt = message.text
    # #bot.send_message(message.chat.id, txt)
    pass


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://que-bot.herokuapp.com/' + token)
    return "!", 200


if __name__ == "__main__":

    if "--debug" in sys.argv:
        bot.remove_webhook()
        bot.polling()
    else:
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

    pass
