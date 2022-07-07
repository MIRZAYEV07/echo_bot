from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import (Updater,ConversationHandler,CommandHandler,CallbackContext,CallbackQueryHandler,MessageHandler,Filters)
from efood_project_db import Database

db = Database()


def make_button(button,holat):



    btn1 = []
    b1 = []
    for a in button:
        b1.append(InlineKeyboardButton(f"{a['name']}",callback_data=f"{holat}_{a['id']}"))
        if len(b1) == 2:
            btn1.append(b1)
            b1 = []
    if b1:
        btn1.append(b1)
    return btn1

def start(update,context):
    print(update)
    db.make_savatcha(update.message.from_user.first_name)

    global user
    user = update.message.from_user.first_name
    if db.get_savatcha(user):
        db.del_savatcha(user)
        db.make_savatcha(update.message.from_user.first_name)

    buttons = [
        [KeyboardButton("🛒 Buyurtma qilish")],
        [KeyboardButton("🛍 Buyurtmalarim"), KeyboardButton("👪 Xodimlar haqida")],
        [KeyboardButton("✍️ Fikr bildirish"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    update.message.reply_text(f"SALOM {update.message.from_user.first_name}",reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
    return 1

def menu(update,context):
    print(update)
    btn = []
    a = make_button(db.get_menu(),"parent")
    print(a)
    btn.extend(a)
    print(btn)

    update.message.reply_text('Tanlang!',reply_markup=InlineKeyboardMarkup(btn))
    return 2

def inline_query(update,context):

    print(update)
    query = update.callback_query
    data = query.data
    if data == 'menu':
        query.message.delete()
        menu(query,context)
    data1 = data.split('_')

    if data1[0] == "parent":
        global c
        c = data1[1]
        btn = []
        a = make_button(db.get_child_menu(int(data1[1])), "child")
        btn.extend(a)
        back = [InlineKeyboardButton("⬅ BACK",callback_data=f"menu")]
        btn.append(back)

        query.message.edit_text('Tanlang!',reply_markup=InlineKeyboardMarkup(btn))
    elif data1[0] == "child":
        global d
        d = data1[1]
        print('asssssssss')

        btn = []
        a = make_button(db.type_1(int(data1[1])), "type")
        btn.extend(a)
        back = [InlineKeyboardButton("⬅ BACK",callback_data=f"parent_{c}")]
        btn.append(back)
        print(data1[1])
        print(btn)
        query.message.delete()
        query.message.reply_text('Tanlang!', reply_markup=InlineKeyboardMarkup(btn))

    elif data1[0] == 'type':
        global qwert
        qwert = data1[1]
        print(f"qwert{data1[1]}")
        print(d)
        print(c)
        b1 = []
        button = [[]]
        for i in range(1,10):
            b1.append(InlineKeyboardButton(f"{i}",callback_data=f"count_{i}"))
            if len(b1) == 3:
                button.append(b1)
                b1 = []
        back =  [InlineKeyboardButton("⬅ BACK",callback_data=f"child_{d}"),
                InlineKeyboardButton("⬆️MENU",callback_data="menu")]
        button.append(back)

        a = db.product(int(d),int(data1[1]))
        global product
        product = a
        info = f"{a['name']}\n {a['about']}\n\n NARXI: {a['price']} so\'m"
        query.message.delete()
        query.message.reply_photo(photo= open(f"{a['photo']}",'rb'),caption = info,reply_markup=InlineKeyboardMarkup(button))

    elif data1[0] == 'count':
        q =  int(data1[1]) * int(product['price'])
        back = [[InlineKeyboardButton("⬅️BACK",callback_data=f"type_{qwert}")]]


        product_list = f"{data1[1]}ta {product['name']} bor!! "
        db.savatcha(product_list,q,user)
        a = db.get_savatcha(user)
        price =  db.get_price(user)
        query.message.delete()
        query.message.reply_text(f"Savatchangizda: \n\n {a} \n\nNARXI:{price} so'm ",reply_markup=InlineKeyboardMarkup(back))




def main():
    TOKEN = "5420058689:AAFYdmLGty31txO_zAFvBZAbXFJMCjDb3vc"

    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start',start)],
        states = {
            1:[MessageHandler(Filters.regex('🛒 Buyurtma qilish'),menu)],
            2:[CallbackQueryHandler(inline_query),CommandHandler('start',start)]

        },
        fallbacks = []
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()