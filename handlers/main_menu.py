from aiogram.types import Message

from keyboards.inline.categories_menu import generate_categories_menu
from loader import db
from router import router


@router.message(lambda message: "📋 Asosiy menyu" == message.text)
async def show_main_menu(message: Message):
    categories = db.get_categories()
    await message.answer_photo(
        photo="https://marketplace.canva.com/EAFKfB87pN0/1/0/1131w/canva-brown-and-black-illustration-fast-food-menu-y8NpubROdFc.jpg",
        caption="Bizning menyu 👇",
        reply_markup=generate_categories_menu(categories)
    )
