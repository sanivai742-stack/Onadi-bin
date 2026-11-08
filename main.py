import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

# আপনার নতুন টেলিগ্রাম বট টোকেন
API_TOKEN = '9027972676:AAFsDj4wBDZfU-gUEfr29umXPyU67wG7Mqk'
bot = telebot.TeleBot(API_TOKEN)

# NP Network API কনফিগারেশন
NP_API_BASE_URL = 'https://www.npnetworkbd.com/api/user'
NP_API_KEY = 'NP-6HXU732PNEATGVFM'

# ইউজার ব্যালেন্স ট্র্যাক করার ডিকশনারি
user_balances = {}

def get_user_balance(user_id):
    return user_balances.get(user_id, 0.0)

def add_user_balance(user_id, amount):
    current = user_balances.get(user_id, 0.0)
    user_balances[user_id] = round(current + amount, 2)

# মূল মেনু (নিচের স্থায়ী বাটন)
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📞 Get Number"),
        KeyboardButton("🔍 Search Number"),
        KeyboardButton("🔥 Proxy/VPN"),
        KeyboardButton("👥 Refer"),
        KeyboardButton("🛡️ 2FA"),
        KeyboardButton("💰 Balance"),
        KeyboardButton("💬 Support"),
        KeyboardButton("💳 Withdrawal")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "💎 *FRD Prime | Premium OTP Service*\n\n"
        "✨ Welcome to Number & OTP Service.\n"
        "👇 Choose an option below to continue:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# Get Number ক্লিক করলে সার্ভিস লিস্ট
@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def handle_get_number(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🇫 FB Forgot"),
        KeyboardButton("🇫 Facebook"),
        KeyboardButton("📸 Instagram"),
        KeyboardButton("📱 WhatsApp"),
        KeyboardButton("🏠 Home")
    )
    bot.send_message(message.chat.id, "📍 *Select a service:*", parse_mode="Markdown", reply_markup=markup)

# সার্ভিস সিলেক্ট করার পর কান্ট্রি লিস্ট (ইতালি ও ফ্রান্সসহ)
@bot.message_handler(func=lambda message: message.text in ["🇫 FB Forgot", "🇫 Facebook", "📸 Instagram", "📱 WhatsApp"])
def handle_service_selection(message):
    service_name = message.text.split(' ')[1]
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(f"🇫🇷 France - {service_name} (4510 hits)"),
        KeyboardButton(f"🇮🇹 Italy - {service_name} (3820 hits)"),
        KeyboardButton(f"🇨🇲 Cameroon - {service_name} (2197 hits)"),
        KeyboardButton(f"🇪🇹 Ethiopia - {service_name} (220 hits)"),
        KeyboardButton(f"🇹🇯 Tajikistan - {service_name} (13 hits)"),
        KeyboardButton("🔙 Back"),
        KeyboardButton("🏠 Home")
    )
    text = (
        f"🌐 *Select a country for {service_name}:*\n\n"
        f"🔥 *Top countries by hits:*\n"
        f"1. 🇫🇷 France (FR) • 4510 hits 🔥\n"
        f"2. 🇮🇹 Italy (IT) • 3820 hits 🔥\n"
        f"3. 🇨🇲 Cameroon (CM) • 2197 hits\n"
        f"4. 🇪🇹 Ethiopia (ET) • 220 hits\n"
        f"5. 🇹🇯 Tajikistan (TJ) • 13 hits"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# ধাপ ১: কান্ট্রি সিলেক্ট করলে নাম্বার শো করবে এবং "Waiting for OTP" দেখাবে
@bot.message_handler(func=lambda message: any(c in message.text for c in ["France", "Italy", "Cameroon", "Ethiopia", "Tajikistan", "Change Number"]))
def handle_number_generation(message):
    phone_number_1 = "+33612345678"  # ডিফল্ট বা এপিআই থেকে আসা নাম্বার
    
    try:
        api_url = f"{NP_API_BASE_URL}?key={NP_API_KEY}&action=getNumber"
        response = requests.get(api_url, timeout=5)
        data = response.json()
        if 'number' in data:
            phone_number_1 = data['number']
    except Exception as e:
        print(f"API Error: {e}")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(f"📞 📋 {phone_number_1}"),
        KeyboardButton("🔄 Check / Simulate OTP Received"),
        KeyboardButton("🔙 Back"),
        KeyboardButton("🏠 Home")
    )
    
    bot.send_message(
        message.chat.id, 
        f"⏳ *Waiting for OTP...*\n\nYour Number: `{phone_number_1}`", 
        parse_mode="Markdown", 
        reply_markup=markup
    )

# হোমে ফেরার হ্যান্ডলার
@bot.message_handler(func=lambda message: message.text == "🏠 Home")
def handle_home(message):
    send_welcome(message)

# বট রান করার জন্য
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()