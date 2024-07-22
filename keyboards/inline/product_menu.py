from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.utils.back import generate_back_button


def generate_product_menu(category_id: int, product_id: int, quantity: int = 1) -> types.InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.row(
        types.InlineKeyboardButton(text="-", callback_data=f"cart-action:decrement:{quantity}:{category_id}:{product_id}"),
        types.InlineKeyboardButton(text=f"{quantity}", callback_data="..."),
        types.InlineKeyboardButton(text="+", callback_data=f"cart-action:increment:{quantity}:{category_id}:{product_id}")
    )
    markup.row(
        types.InlineKeyboardButton(text="✅🛒 Savatchaga qo'shish", callback_data=f"cart-action:add-to-cart:{quantity}:{category_id}:{product_id}")
    )
    markup.row(
        generate_back_button(destination=f"products:{category_id}")
    )

    return markup.as_markup()
