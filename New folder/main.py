import telebot
from config import token
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(token)

# ========== Welcome + Button ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = KeyboardButton('Product')
    button2 = KeyboardButton('Contact Us')
    markup.add(button1, button2)
    bot.send_message(chat_id=message.chat.id, text="Welcome to MegaPixel Store!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Product')
def send_image(message):
    try:
        photo = open('offer.jpg', 'rb')  # Image file must exist in same folder
        bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Image not found. Please check 'offer.jpg'.")

@bot.message_handler(func=lambda message: message.text == 'Contact Us')
def send_image(message):
        phone ='07717349858'
        bot.send_message(message.chat.id, phone)

user_map = {}
YOUR_TELEGRAM_ID = 643262525  # Replace with your Telegram ID

# Forward user messages to YOU
@bot.message_handler(func=lambda m: m.chat.id != YOUR_TELEGRAM_ID, content_types=['text', 'photo', 'video', 'document', 'audio'])
def forward_to_owner(message):
    forwarded = bot.forward_message(chat_id=YOUR_TELEGRAM_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    user_map[(YOUR_TELEGRAM_ID, forwarded.message_id)] = message.chat.id
    bot.send_message(chat_id=message.chat.id, text="We received your message!")

# Handle YOUR reply to forwarded message
@bot.message_handler(func=lambda m: m.chat.id == YOUR_TELEGRAM_ID and m.reply_to_message is not None)
def reply_from_owner(message):
    forwarded_msg_id = message.reply_to_message.message_id
    key = (YOUR_TELEGRAM_ID, forwarded_msg_id)

    if key in user_map:
        original_user_id = user_map[key]
        bot.send_message(original_user_id, message.text)
    else:
        bot.send_message(YOUR_TELEGRAM_ID, "❌ Could not find the original user.")

# ========== Start the Bot ==========
bot.polling()