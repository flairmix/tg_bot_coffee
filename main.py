from replit import db
import os
import telebot
from datetime import date, timedelta

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['help'])
def help(message):
    str_output = "Привет, маленький беспомощный любитель кофе! \n\
    \n\
    Лист комманд: \n\
    \\list - показать историю оплат за кофе;\n\
    \\add_pay_{name} - вписать оплату за кофе за сегодня;\n\
    \\queue - показать {name}, чья куеуе сегодня платить; \n\
    \\queue_next - сдвинуть очередь на следующего;\n\
    \n\
    отзывы и предложения не принимаются ;)"

    bot.send_message(message.chat.id, str_output)


@bot.message_handler(commands=['version'])
def version(message):
    version = 0.1
    version_date = "21/11/01"
    str_output = "version - " + str(version) + " - " + version_date
    str_output += "\n \n - запись людей в список с датой - сегодня"
    str_output += "\n - вывод списка людей с датой "
    str_output += "\n - вывод очереди "
    str_output += "\n - сдвиг очереди вправо"
    bot.send_message(message.chat.id, str_output)


def check_day_for_pay(date_str, check_date):
    if date_str == check_date.strftime('%Y/%m/%d'):
        return True
    else:
        return False


def output_day_pay(day, user):
    return (day.strftime('%Y/%m/%d/%A') + " --> " + str(user) + "\n")


def add_pay_user(user):
    user = db["users"].get(user)
    user.append(date.today().strftime('%Y/%m/%d'))


def check_double_pay_day():
    check_day = date.today()
    for user in db["users"]:
        userdata = db["users"].get(user)

        for i in range (0, len(userdata), 1):
            if check_day_for_pay(userdata[i], check_day):
                return True
    return False

 
@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "hello!")


#show history list for 5 days payments
@bot.message_handler(commands=['list'])
def list(message):
    tx_list = ["" for i in range(5)]

    check_day = date.today()

    for user in db["users"]:
        userdata = db["users"].get(user)

        for i in range (0, len(userdata), 1):
            for j in range (5):
                if check_day_for_pay(userdata[i], (check_day- timedelta(days=j))):
                    tx_list[j] = output_day_pay(check_day - timedelta(days=j), user)

    tx = tx_list[0] + tx_list[1] + tx_list[2] + tx_list[3] + tx_list[4]

    bot.send_message(message.chat.id, tx)


#create or reset database payments
@bot.message_handler(commands=['create_coffee_lovers'])
def create_coffee_lovers(message):
    db["users"] = {
        "mid": ["2021/10/28"],
        "laz": ["2021/10/25"],
        "kir": ["2021/10/26"],
        "dae": ["2021/10/27", "2021/10/29"]
        }
    bot.send_message(message.chat.id, "done")

    
#start or reset queue people payments 
@bot.message_handler(commands=['create_queue'])
def create_queue(message):
    db["queue"] = "mid"
    bot.send_message(message.chat.id, "queue_start_today_with_mid")

    
#show queue today 
@bot.message_handler(commands=['queue'])
def queue(message):
    text = date.today().strftime('%Y/%m/%d/%A') + " -- queue -- " + str(db["queue"])
    bot.send_message(message.chat.id, text)


#move queue in next position (rigth)
@bot.message_handler(commands=['queue_next'])
def queue_next(message):
    list_users = ["mid", "laz", "kir", "dae"]
    for i in list_users:
        if i == db["queue"]:
            index = list_users.index(db["queue"])
            if index != 3:
                db["queue"] = list_users[index+1]
                tx_output = "next in queue - " + str(db["queue"] )
                bot.send_message(message.chat.id, tx_output)
                break
            else:
                db["queue"] = list_users[0]
                tx_output = "next in queue - " + str(db["queue"] )
                bot.send_message(message.chat.id, tx_output)
                break


#user_pay_history
@bot.message_handler(commands=['pay_mid'])
def pay(message):
    user = db["users"].get("mid")
    tx = ""
    for i in user:
        tx += i + "\n"
    bot.send_message(message.chat.id, tx)



#add pay today ----------------------------------

@bot.message_handler(commands=['add_pay_mid'])
def add_pay_mid(message):
    if not check_double_pay_day():
        add_pay_user("mid")
        bot.send_message(message.chat.id, "mid_paid" )
    else:
        bot.send_message(message.chat.id, "mid_not_paid" )

@bot.message_handler(commands=['add_pay_kir'])
def add_pay_kir(message):
    if not check_double_pay_day():
        add_pay_user("kir")
        bot.send_message(message.chat.id, "kir_paid")
    else:
        bot.send_message(message.chat.id, "kir_not_paid" )

@bot.message_handler(commands=['add_pay_laz'])
def add_pay_laz(message):
    if not check_double_pay_day():
        add_pay_user("laz")
        bot.send_message(message.chat.id, "laz_paid")
    else:
        bot.send_message(message.chat.id, "kir_not_paid" )

@bot.message_handler(commands=['add_pay_dae'])
def add_pay_dae(message):
    if not check_double_pay_day():    
        add_pay_user("dae")
        bot.send_message(message.chat.id, "dae_paid")
    else:
        bot.send_message(message.chat.id, "kir_not_paid" )

#----------------------------------

bot.polling()
