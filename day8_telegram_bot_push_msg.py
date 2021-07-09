import telebot

chat_id = "YOUR_CHAT_ID"
bot = telebot.TeleBot("TOKEN", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
bot.send_message(chat_id, "這則訊息由 Bot 主動發送的喔～")