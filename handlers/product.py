from aiogram import types

from router import router
from loader import db
from keyboards.inline.product_menu import generate_product_menu


@router.callback_query(lambda call: "product" in call.data)
async def show_product_details(call: types.CallbackQuery):
    product_id = int(call.data.split(":")[-1])  # "product:1" => ["product", "1"]
    product = db.get_product(product_id=product_id)

    price = f"{int(product.get('price')):,}".replace(",", " ")
    caption = f"{product.get('name')}\n\n{product.get('description')}\n\nNarxi: {price} so'm"

    await call.message.delete()
    await call.message.answer_photo(
        photo=product.get('photo'),
        caption=caption,
        reply_markup=generate_product_menu(
            category_id=product.get('category_id'),
            product_id=product_id)
    )
