
import logging

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext, CallbackQueryHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
total_count = 0
which_quiz_flag = 0
current_question = 0

title_it = ['Сервіс з допомогою якого можна організовувати різні опитування це',
            'Який з наведених нижче тегів не використовується для форматування тексту?',
            'Щоб додати зображення на сторінку можна використати тег з атрибутом:',
            'Щоб браузер відкривав сторінку за посиланням в новій вкладці (або вікні), використовують:']
keyboards_it = [[[
    InlineKeyboardButton("Google документ", callback_data="0"),
    InlineKeyboardButton("Google Сайти", callback_data="0"),
    InlineKeyboardButton("Google Форми", callback_data="1"),
]], [[
    InlineKeyboardButton("< strong >", callback_data="0"),
    InlineKeyboardButton("< em >", callback_data="0"),
    InlineKeyboardButton("< span >", callback_data="1"),
]], [[
    InlineKeyboardButton("img; src", callback_data="0"),
    InlineKeyboardButton("photo; href;", callback_data="0"),
    InlineKeyboardButton("img; href;", callback_data="1"),
]], [[
    InlineKeyboardButton("атрибут blank.", callback_data="0"),
    InlineKeyboardButton("атрибут target;", callback_data="0"),
    InlineKeyboardButton("тег target;", callback_data="1"),
]]]

title_medicine = ['Що зміцнює ваше здоров',
                  'Яка система органів людини потребуватиме лікування у випадку перелому руки?',
                  'Яка система органів людини потребуватиме лікування у випадку пневмонії ?',
                  'Яка система органів людини потребуватиме лікування у випадку харчового отруєння?']
keyboards_medicine = [[[
    InlineKeyboardButton("фізична активність", callback_data="1"),
    InlineKeyboardButton("комп'ютерні ігри", callback_data="0"),
    InlineKeyboardButton("сон 4 години", callback_data="0"),
]], [[
    InlineKeyboardButton("нервова", callback_data="0"),
    InlineKeyboardButton("травна", callback_data="0"),
    InlineKeyboardButton("опорно-рухова", callback_data="1"),
]], [[
    InlineKeyboardButton("нервова", callback_data="0"),
    InlineKeyboardButton("кровоносна", callback_data="0"),
    InlineKeyboardButton("дихальна", callback_data="1"),
]], [[
    InlineKeyboardButton("дихальна", callback_data="0"),
    InlineKeyboardButton("кровоносна", callback_data="0"),
    InlineKeyboardButton("травна", callback_data="1"),
]]]


def start(update: Update, context: CallbackContext) -> None:
    buttons = [[(KeyboardButton("Опитування по Інформатиці"))], [(KeyboardButton("Опитування по Медецині"))]]
    reply_markup = ReplyKeyboardMarkup(buttons)
    update.effective_chat.send_message(text=str("Оберіть опитування. "), reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    global total_count
    global current_question
    query = update.callback_query

    query.answer()
    query.message.edit_reply_markup()

    if current_question == len(keyboards_it) - 1:
        if total_count < 2 and which_quiz_flag == 1:
            query.message.reply_text(text="Ви погано знаєтесь на медицині")
        if total_count >= 2 and which_quiz_flag == 1:
            query.message.reply_text(text="Ви добре знаєтесь на медицині")
        if total_count < 2 and which_quiz_flag == 0:
            query.message.reply_text(text="Ви погано знаєтесь на інформатиці")
        if total_count >= 2 and which_quiz_flag == 0:
            query.message.reply_text(text="Ви добре знаєтесь на інформатиці")
    elif which_quiz_flag == 0:
        logger.info(current_question)
        reply_markup = InlineKeyboardMarkup(keyboards_it[current_question + 1])
        query.message.reply_text(title_it[current_question + 1], reply_markup=reply_markup)
    elif which_quiz_flag == 1:
        reply_markup = InlineKeyboardMarkup(keyboards_medicine[current_question + 1], )
        query.message.reply_text(title_medicine[current_question + 1], reply_markup=reply_markup)

    total_count += int(query.data)
    current_question += 1


def messageAnswerCustomHandler(update: Update, context: CallbackContext) -> None:
    global which_quiz_flag
    global total_count
    global current_question
    total_count = 0
    current_question = 0
    if update.message.text == "Опитування по Інформатиці":
        reply_markup = InlineKeyboardMarkup(keyboards_it[current_question])
        which_quiz_flag = 0
        update.message.reply_text(title_it[current_question], reply_markup=reply_markup)
    if update.message.text == "Опитування по Медецині":
        reply_markup = InlineKeyboardMarkup(keyboards_medicine[current_question])
        which_quiz_flag = 1
        update.message.reply_text(title_medicine[current_question], reply_markup=reply_markup)


def main() -> None:
    updater = Updater("5409047172:AAGci2HmXRlheqwJ6wztPG9PEyUso9sbKD4")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, messageAnswerCustomHandler))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
