from aiogram import types

from keyboards.inline.product_menu import generate_product_menu
from keyboards.inline.categories_menu import generate_categories_menu
from router import router
from loader import db


@router.callback_query(lambda call: "cart-action" in call.data)
async def cart_action(call: types.CallbackQuery):
    action = call.data.split(":")[1]
    quantity = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    product_id = int(call.data.split(":")[4])
    new_quantity = quantity

    if action == "increment":
        new_quantity = quantity + 1

    elif action == "decrement":
        if quantity - 1 > 0:
            new_quantity = quantity - 1

    elif action == "add-to-cart":
        # user ni aniqlab olish
        user = db.get_user(telegram_id=call.from_user.id)

        # kategoriyalarni olish
        categories = db.get_categories()

        # Maxsulotni savatchaga saqlash
        db.add_product_to_cart(
            user_id=user.get("id"),
            product_id=product_id,
            quantity=quantity,
        )
        await call.message.delete()
        await call.answer(text="✅ Maxsulot savatchaga qo'shildi", show_alert=True)
        await call.message.answer_photo(
            photo="https://marketplace.canva.com/EAFKfB87pN0/1/0/1131w/canva-brown-and-black-illustration-fast-food-menu-y8NpubROdFc.jpg",
            caption="Bizning menyu 👇",
            reply_markup=generate_categories_menu(categories)
        )

    if quantity - 1 != 0 or action == "increment":
        await call.message.edit_reply_markup(
            reply_markup=generate_product_menu(
                category_id=category_id,
                product_id=product_id,
                quantity=new_quantity,
            )
        )
