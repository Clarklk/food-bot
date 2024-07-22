import datetime

from aiogram.types import CallbackQuery, LabeledPrice, ShippingQuery, ShippingOption, PreCheckoutQuery

from config import PAYMENT_TOKEN
from keyboards.inline.cart import generate_cart_menu
from loader import db, bot
from router import router


@router.callback_query(lambda call: "overall-actions" in call.data)
async def overall_actions(call: CallbackQuery):
    user = db.get_user(telegram_id=call.from_user.id)
    splitted_call = call.data.split(":")  # ["cart-actions", "increment", "1", ...]
    action = splitted_call[1]
    order_id = splitted_call[2]
    product_id = splitted_call[3]
    quantity = int(splitted_call[4])
    new_quantity = 0

    telegram_id = call.from_user.id
    user_id = db.get_user(telegram_id=telegram_id).get('id')

    if action == "increment":
        new_quantity = quantity + 1
        db.update_cart_product_quantity(user_id=user_id, product_id=product_id, new_quantity=new_quantity)

    elif action == "decrement":
        new_quantity = quantity - 1

        if new_quantity < 1:
            new_quantity = 1
        db.update_cart_product_quantity(user_id=user_id, product_id=product_id, new_quantity=new_quantity)

    elif action == "show":
        product = db.get_product(product_id=product_id)
        total_price = int(product.get('price')) * quantity
        total_price = f'{total_price:,}'.replace(',', ' ')

        await call.answer(
            text=f"{product.get('name')}, {product.get('price')} x {quantity} = {total_price} so'm",
            show_alert=True)

    elif action == "delete":
        db.delete_cart_product(order_id=order_id)
        cart_products = db.get_cart_products(user_id=user_id)

        if len(cart_products) < 1:
            text = "Sizning savatchangiz bo'sh 🧐"

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

        await call.message.edit_text(
            text=text,
            reply_markup=generate_cart_menu(cart_products=cart_products)
        )

    elif action == "continue":
        cart_products = db.get_cart_products(user_id=user.get("id"))
        text = ""

        total_price = 0
        prices = []

        for index, cart_product in enumerate(cart_products, start=1):
            product = db.get_product(product_id=cart_product.get("product_id"))
            quantity = cart_product.get("quantity")

            product_total_price = int(product.get("price")) * int(quantity)
            total_price += product_total_price
            prices.append(
                LabeledPrice(label=product.get("name"),
                             amount=int(product.get("price")) * 100)
            )

            text += f"{index}. {product.get('name')}, x{quantity} = {f'{product_total_price:,}'.replace(',', ' ')} so'm\n"

        text += f"\nUmumiy narx: {f'{total_price:,}'.replace(',', ' ')} so'm"

        await bot.send_invoice(
            chat_id=call.from_user.id,
            title="🛒 Sizning savatchangiz",
            description="Description of the items",
            payload="some payload",
            provider_token=PAYMENT_TOKEN,
            currency="UZS",
            prices=prices,
            need_shipping_address=True,
            need_name=True,
            need_email=True,
            need_phone_number=True,
            is_flexible=True,
            start_parameter="sadrbek-food-delivery-bot",
            suggested_tip_amounts=[1000 * 100, 2000 * 100, 5000 * 100],
            max_tip_amount=5000 * 100
        )

    if action in ["increment", "decrement"] and quantity != new_quantity:
        cart_products = db.get_cart_products(user_id=user_id)

        text = "🛒 Sizning savatchangiz:\n\n"

        total_price = 0
        for index, cart_product in enumerate(cart_products, start=1):
            product = db.get_product(product_id=cart_product.get("product_id"))
            quantity = cart_product.get("quantity")

            product_total_price = int(product.get('price')) * int(quantity)
            total_price += product_total_price

            text += f"{index}. {product.get('name')}, x{quantity} = {f'{product_total_price:,}'.replace(',', ' ')} so'm\n"

        text += f"\nUmumiy narx: {f'{total_price:,}'.replace(',', ' ')} so'm"

        await call.message.edit_text(
            text=text,
            reply_markup=generate_cart_menu(cart_products=cart_products)
        )


@router.shipping_query()
async def show_shipping_options(shipping_query: ShippingQuery):
    await shipping_query.answer(
        ok=True,
        shipping_options=[
            ShippingOption(id="slow", title="Standart yetkazish",
                           prices=[LabeledPrice(label="Standart yetkazish", amount=10_000 * 100)]),
            ShippingOption(id="fast", title="Uchib yetkazib berish",
                           prices=[LabeledPrice(label="Uchib yetkazib berish", amount=50_000 * 100)]),
        ]
    )


@router.pre_checkout_query(lambda query: True)
async def checkout(pre_checkout_query: PreCheckoutQuery):
    telegram_id = pre_checkout_query.from_user.id
    user = db.get_user(telegram_id=telegram_id)
    user_cart_products = db.get_cart_products(user_id=user.get("id"))

    # Savatcha maxsulotlarini buyurtmalar tarixiga qo'shish
    for user_cart_product in user_cart_products:
        product_id = user_cart_product.get("product_id")
        product = db.get_product(product_id=product_id)

        quantity = product.get("quantity")
        total_price = int(product.get("price")) * quantity

        date = str(datetime.datetime.now().date())
        time = str(datetime.datetime.now().time())

        print(date)
        print(time[:8])

        db.add_to_orders_history(user_id=user.get("id"), product_id=product_id, quantity=quantity, total_price=total_price, time=created_time, date=created_date)

    # Foydalanuvchi savatchasini tozalab yuborish
    db.clear_user_cart(user_id=user.get("id"))
    
    await pre_checkout_query.answer(
        ok=True,
        # error_message="To'lov jarayonida xatolik ketdi yoki maxsulot omborda qolmagan",
    )
