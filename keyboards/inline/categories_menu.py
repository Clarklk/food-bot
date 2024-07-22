from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def generate_categories_menu(categories: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    for category in categories:
        markup.button(text=category.get("name"), callback_data=f"category:{category.get('id')}")
    markup.adjust(2)

    return markup.as_markup()
