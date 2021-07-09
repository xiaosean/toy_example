import telebot

bot = telebot.TeleBot("TOKEN") # 定義機器人

@bot.message_handler(commands=['start', 'help']) # 當輸入 start, help 的指令會發佈到這裡
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['chatid']) # 不管什麼指令都會回這句話
def my_chat_id(message):
    print(f"Received message = {message}")
    chat_id = message.chat.id
    bot.reply_to(message, f"本對話之 chat id 為 {chat_id}, 此 id 可供你主動推播訊息至本對話窗")
    
@bot.message_handler(func=lambda message: True) # 不管什麼指令都會回這句話
def echo_all(message):
    your_text = message.text
    bot.reply_to(message, f"你的指令是 {your_text}")

bot.polling() # 執行程式