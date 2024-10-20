import telebot
import time
import threading

# Initialize the bot with your API token
API_TOKEN = '8034830634:AAG8NJlCCrzPeBGsVhoCnZe1IRcLoLgkpKs'  # Replace with your bot API token
bot = telebot.TeleBot(API_TOKEN)

# To control the sending of messages
sending_thread = None
sending_active = False

# Function to send "Hi" every 5 seconds
def send_hi(chat_id):
    global sending_active
    while sending_active:
        bot.send_message(chat_id, "Hi")
        time.sleep(5)

# Start command handler
@bot.message_handler(commands=['start'])
def start_sending(message):
    global sending_active, sending_thread
    if not sending_active:
        sending_active = True
        bot.send_message(message.chat.id, "I will send 'Hi' every 5 seconds. Type /stop to stop me.")
        
        # Start a new thread to send messages
        sending_thread = threading.Thread(target=send_hi, args=(message.chat.id,))
        sending_thread.start()
    else:
        bot.send_message(message.chat.id, "I'm already sending 'Hi' every 5 seconds!")

# Stop command handler
@bot.message_handler(commands=['stop'])
def stop_sending(message):
    global sending_active, sending_thread
    if sending_active:
        sending_active = False
        if sending_thread is not None:
            sending_thread.join()  # Wait for the thread to finish
            sending_thread = None
        bot.send_message(message.chat.id, "Stopping the 'Hi' messages.")
    else:
        bot.send_message(message.chat.id, "I'm not sending any messages right now.")

# Start polling
if __name__ == '__main__':
    bot.polling(none_stop=True)
