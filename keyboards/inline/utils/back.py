from aiogram.types import InlineKeyboardButton


def generate_back_button(destination: str) -> InlineKeyboardButton:
    back_button = InlineKeyboardButton(
        text="👈 Orqaga", callback_data=f"back:{destination}"
    )

    return back_button
