from aiogram import types

from router import router
from loader import db
from keyboards.inline.products_menu import generate_products_menu


@router.callback_query(lambda call: "category" in call.data)
async def show_products_menu(call: types.CallbackQuery):
    category_id = int(call.data.split(":")[-1])
    products = db.get_products(category_id)

    if len(products) == 0:
        await call.answer("Ushbu kategoriya bo'yicha maxsulot topilmadi", show_alert=True)
    else:
        await call.message.delete()
        await call.message.answer_photo(photo="https://avatars.dzeninfra.ru/get-zen_doc/5042448/pub_62065c9a29517f642969368e_62065eb5d54c99747d845bb4/scale_1200",
                                        caption="Ushbu kategoriya bo'yicha axsulotlar",
                                        reply_markup=generate_products_menu(products))
