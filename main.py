import requests, schedule, telebot, os
from time import sleep
from threading import Thread
from alive import keep_alive

keep_alive()

ids = [1060264505, -1001595229368] #ID's of Groups to send the message in case new burn is tracked
botkey = os.environ['botkey']
bscapi = os.environ['bscapi']
bot = telebot.TeleBot(botkey, parse_mode="HTML")
#bot.send_message(-1001595229368, "Update!")

def check_burnt():
    data = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xaFb64E73dEf6fAa8B6Ef9a6fb7312d5C4C15ebDB&address=0x000000000000000000000000000000000000dead&tag=latest&apikey="+bscapi).json()
    totalsupply = requests.get("https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xaFb64E73dEf6fAa8B6Ef9a6fb7312d5C4C15ebDB&apikey="+bscapi).json()
    burnt_token = data['result'][:-18]
    tsupply = totalsupply['result'][:-18]
    csupply = int(tsupply)-int(burnt_token)
    burnt_old = ""
    with open("info.py", 'r') as det:
        burnt_old = det.read()
    if burnt_old != burnt_token:
        new_burnt = int(burnt_token)-int(burnt_old)
        with open("info.py", "w") as det:
            det.write(burnt_token)
        burnmsg = f"""<b><ins>Grove Tokens Burnt!!🔥🔥🔥</ins></b>
💰 <b>No. of newly burned:</b> {int(new_burnt):,}
💎 <b>Total amount of GVR burnt to date:</b> {int(burnt_token):,}
⚖️ <b>Current Circulating Supply:</b> {csupply:,}"""
        for id in ids:
            bot.send_message(id, burnmsg)
        print(burnt_token)
    else:
        return False

schedule.every(4).minutes.do(check_burnt)

def forever():
    while True:
        schedule.run_pending()
        sleep(1)

t1 = Thread(target = forever)
t1.start()

@bot.message_handler(commands=['start', 'help'])
def start_msg(msg):
    bot.reply_to(msg, "Bot to track burn related info for GVR Token, functions in group.\nMade by @DevAdvik")

@bot.message_handler(commands=['burn'])
def gimmeburn(msg):
    data = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xaFb64E73dEf6fAa8B6Ef9a6fb7312d5C4C15ebDB&address=0x000000000000000000000000000000000000dead&tag=latest&apikey="+bscapi).json()
    totalsupply = requests.get("https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xaFb64E73dEf6fAa8B6Ef9a6fb7312d5C4C15ebDB&apikey="+bscapi).json()
    tsupply = totalsupply['result'][:-18]
    burnt_token = data['result'][:-18]
    csupply = int(tsupply)-int(burnt_token)
    burnmsg = f"""<b><ins>Grove Tokens Burnt🔥🔥🔥</ins></b>
💎 <b>Total amount of GVR burnt to date:</b> {int(burnt_token):,}
⚖️ <b>Current Circulating Supply:</b> {csupply:,}"""
    bot.send_message(msg.chat.id, burnmsg)

@bot.message_handler(commands=['dev'])
def whomadeu(msg):
    bot.reply_to(msg, "This bot is made by @istoleabread")

    
bot.infinity_polling(skip_pending=True)
