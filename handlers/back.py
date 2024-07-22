from aiogram import types

from keyboards.inline.categories_menu import generate_categories_menu
from keyboards.inline.products_menu import generate_products_menu
from loader import db
from router import router


@router.callback_query(lambda call: "back" in call.data)
async def handle_back(call: types.CallbackQuery):
    destination = call.data.split(":")[1]

    if destination == "main_menu":
        categories = db.get_categories()
        await call.message.delete()
        await call.message.answer_photo(
            photo="https://marketplace.canva.com/EAFKfB87pN0/1/0/1131w/canva-brown-and-black-illustration-fast-food-menu-y8NpubROdFc.jpg",
            caption="Bizning menyu 👇",
            reply_markup=generate_categories_menu(categories)
        )

    elif destination == "products":
        category_id = int(call.data.split(":")[-1])
        products = db.get_products(category_id=category_id)

        if len(products) == 0:
            await call.answer("Ushbu kategoriya bo'yicha maxsulot topilmadi", show_alert=True)
        else:
            await call.message.delete()
            await call.message.answer_photo(
                photo="https://avatars.dzeninfra.ru/get-zen_doc/5042448/pub_62065c9a29517f642969368e_62065eb5d54c99747d845bb4/scale_1200",
                caption="Ushbu kategoriya bo'yicha axsulotlar",
                reply_markup=generate_products_menu(products))
