from aiogram import types

from keyboards.inline.cart import generate_cart_menu
from loader import db
from router import router


@router.message(lambda message: "/cart" == message.text)
@router.message(lambda message: "🛒 Savatcham" == message.text)
async def show_cart(message: types.Message):
    user = db.get_user(telegram_id=message.from_user.id)
    cart_products = db.get_cart_products(user_id=user.get("id"))

    if len(cart_products) == 0:
        await message.answer(text="Sizning savatchangiz bo'sh 🧐")

    else:
        text = "🛒 Sizning savatchangiz:\n\n"

        total_price = 0
        for index, cart_product in enumerate(cart_products, start=1):
            product = db.get_product(product_id=cart_product.get("product_id"))
            quantity = cart_product.get("quantity")

            product_total_price = int(product.get('price')) * int(quantity)
            total_price += product_total_price

            text += f"{index}. {product.get('name')}, x{quantity} = {f'{product_total_price:,}'.replace(',', ' ')} so'm\n"

        text += f"\nUmumiy narx: {f'{total_price:,}'.replace(',', ' ')} so'm"

        await message.answer(
            text=text,
            reply_markup=generate_cart_menu(cart_products=cart_products)
        )
