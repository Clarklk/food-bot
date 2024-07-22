from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from keyboards.inline.utils.back import generate_back_button


def generate_products_menu(products: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    for product in products:
        markup.button(text=product.get("name"), callback_data=f"product:{product.get('id')}")
    markup.adjust(2)
    markup.row(
        generate_back_button(destination="main_menu")
    )

    return markup.as_markup()
