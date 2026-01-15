import telebot
from telebot import types
from openpyxl import Workbook
import os
TOKEN="8437298669:AAGmPG9d8c5MkPJ4P4stu-QMG0MLObYjVhI"
bot=telebot.TeleBot(TOKEN)
ADMIN=[8288153487]
ADMIN_ID={
    8288153487:"SULTONOV ODAMBOY"
    }
users={}
user=[]
channels=[]
state_admin={
    "state":0
    }
ch={}
code={"code":None}   
def Follow(message):
    chat_id=message.chat.id
    ABC=types.InlineKeyboardMarkup()
    ABC.add(
        types.InlineKeyboardButton("Uyga Vazifa", callback_data="home"),
        types.InlineKeyboardButton("Sinov Test", callback_data="exam"),
        types.InlineKeyboardButton("Davomat", callback_data="davomat")
        )
    bot.send_message(chat_id, "O`zingizga kerakli bo`limni tanlang", reply_markup=ABC)
    
    
def send_channel_buttons(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for kanal in channels:
        button = types.InlineKeyboardButton(
            text=f"{kanal} kanaliga kirish",
            url=f"https://t.me/{kanal.strip('@')}"
        )
        markup.add(button)
        # Tekshirish tugmasi ham inline tugma sifatida
    check_btn = types.InlineKeyboardButton(
        text="✅ Kanallarga a’zolikni tekshir",
        callback_data="check_channels"
    )
    markup.add(check_btn)
    bot.send_message(chat_id, "Iltimos, quyidagi kanallarga a'zo bo'ling va tugmani bosing", reply_markup=markup)

# 2️⃣ Kanal a’zoligini tekshirish funksiyasi
def check_channel_membership(chat_id):
    for kanal in channels:
        try:
            member = bot.get_chat_member(kanal, chat_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    chat_id=message.chat.id
    if chat_id in ADMIN:
        ch[chat_id]={
            "state":0
            }
        Admin_button_start=types.ReplyKeyboardMarkup(resize_keyboard=True)
        Admin_button_start.add("Admin qo`shish", "Kanal qo`shish")
        Admin_button_start.add("Foydalanuvchilar ro`yxati", "Davomat"),
        Admin_button_start.add("Uyga vazifa", "Sinov testlar")
        Admin_button_start.add(" Botda xabar yuborish ", "Reklama")
        bot.send_message(chat_id, f"Bot admini {ADMIN_ID[chat_id]}, o`zingizga kerakli bo`limni tanlashingiz mumkin", reply_markup=Admin_button_start)
    else:
        user.append(chat_id)
        users[chat_id]={
            "state":"name",
            "name":None,
            "phone":None
            }
        bot.send_message(chat_id, " Ismingiz va Familiyangizni kiriting ")
        users[chat_id]["state"]="phone" 
         
@bot.message_handler(func=lambda m: m.from_user.id in ADMIN)
def Admin_panel(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Admin qo`shish" and chat_id in ADMIN:
        state_admin["state"] = "admin_id"
        bot.send_message(
            chat_id,
            "Iltimos, admin qilmoqchi bo‘lgan insoningizning Telegram ID sini yozing"
        )
        return

    if state_admin.get("state") == "admin_id":
        try:
            admin_id = int(text)
        except ValueError:
            bot.send_message(chat_id, "❌ Iltimos, faqat raqam kiriting")
            return

        ADMIN.append(admin_id)
        state_admin["admin_id"] = admin_id   # ⭐ ID ni saqlab qo‘yamiz
        state_admin["state"] = "admin_name"

        bot.send_message(chat_id, "Admin ismini yozib yuboring")
        return

    if state_admin.get("state") == "admin_name":
        admin_id = state_admin["admin_id"]
        ADMIN_ID[admin_id] = text

        state_admin["state"] = None
        state_admin.pop("admin_id", None)

        bot.send_message(
            chat_id,
            "✅ Foydalanuvchi bot admini sifatida qabul qilindi"
        )
        return
    if chat_id in ADMIN and text=="Foydalanuvchilar ro`yxati":
        with open("Users.txt", "r", encoding="utf-8") as fayl:
            for line in fayl: 
                bot.send_message(chat_id, f"{line}")
            
        
    if chat_id in ADMIN and text=="Kanal qo`shish":
        ch[chat_id]={"state":1}
        bot.send_message(chat_id, "Kanal ssilkasini @Telegramkanal ko`rinishida yuboring")
        return
    if chat_id in ADMIN and ch[chat_id]["state"]==1:
        channels.append(text)
        bot.send_message(chat_id, " Qabul qilindi ")
        ch[chat_id]["state"]=0
        return
    if chat_id in ADMIN and text =="Davomat":
        Admin_button_start=types.ReplyKeyboardRemove()
        code["code"]="code"
        bot.send_message(chat_id, " Iltimos foydalanuvchilarni davomatdan o`tkazish uchun kod kiriting", reply_markup=Admin_button_start)
        return
    if chat_id in ADMIN and code["code"]=="code":
        code["code"]=text
        wb = Workbook()
        ws = wb.active
        ws.title = "Davomat"
        ws.append(["User ID", "Ism va Familiya", "Telefon"])
        wb.save("Davomat.xlsx")
        Code=types.ReplyKeyboardMarkup(resize_keyboard=True)
        Code.add("Davomatni to`xtatish")
        bot.send_message(chat_id, "Kod qabul qilindi", reply_markup=Code)
        return
    if chat_id in ADMIN and text=="Davomatni to`xtatish":
        code["code"]=None
        Code=types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "Davomat to`xtatildi", reply_markup=Code)
        with open("Davomat.xlsx", "rb") as file:
            bot.send_document(message.chat.id, file)
            return start(message)
        
            

@bot.message_handler(func=lambda m:True)
def Register(message):
    chat_id=message.chat.id
    if users[chat_id]["state"]=="phone":
        users[chat_id]["name"]=message.text
        button=types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone=types.KeyboardButton(" Telefon raqam ", request_contact=True)
        button.add(phone)
        bot.send_message(chat_id, " Telefon raqamingizni yuboring ", reply_markup=button)
        
@bot.message_handler(content_types=['contact'])
def Phone(message):
    chat_id=message.chat.id
    if chat_id not in ADMIN:
        users[chat_id]["phone"]=message.contact.phone_number
        button=types.ReplyKeyboardRemove()
        with open("Users.txt", "a") as fayl:
            fayl.write(f"Ism va familiya: {users[chat_id]["name"]}\n Telefon raqam:  {users[chat_id]["phone"]}\n ID: {chat_id}\n")
        bot.send_message(chat_id, f"Ro`yxatdan o`tish yakunlandi\n Sizning ism va familiyangiz: {users[chat_id]["name"]}\n Telefon raqamingiz:  {users[chat_id]["phone"]}", reply_markup=button)
        send_channel_buttons(chat_id)

# 4️⃣ /check handler: kanal a’zoligini tekshirish
@bot.message_handler(commands=['check'])
def check(message):
    chat_id = message.chat.id
    if check_channel_membership(chat_id):
        bot.send_message(chat_id, "✅ Siz barcha kanallarga a'zo bo‘lgansiz. Botni ishlatishingiz mumkin.")
    else:
        bot.send_message(chat_id, "❌ Siz hali barcha kanallarga a'zo emassiz. Iltimos, barcha kanallarga a'zo bo'ling.")
        send_channel_buttons(chat_id)
        check_channel_membership(chat_id)
@bot.callback_query_handler(func=lambda call: call.data == "check_channels")
def callback_check_channels(call):
    chat_id = call.message.chat.id
    if check_channel_membership(chat_id):
        bot.answer_callback_query(call.id, "✅ Siz barcha kanallarga a'zo bo‘ldingiz!")
        return Follow(call)
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali barcha kanallarga a'zo emassiz!")
        bot.send_message(chat_id, "Siz hali barcha kanallarga a'zo emassiz. Iltimos, barcha kanallarga a'zo bo'ling.")
        send_channel_buttons(chat_id)  # Inline tugmalarni qayta yuborish    
    
bot.infinity_polling()