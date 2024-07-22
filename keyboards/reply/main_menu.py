from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def generate_main_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()

    markup.button(text="📋 Asosiy menyu")
    markup.row(
        KeyboardButton(text="📑 Buyurtmalar tarixi"),
        KeyboardButton(text="🛒 Savatcham")
    )

    return markup.as_markup(resize_keyboard=True)
