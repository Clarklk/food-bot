from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


def generate_cart_menu(cart_products: list) -> InlineKeyboardMarkup:
    """
    Returns cart menu to increase, decrease or remove any cart product
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardBuilder()

    for cart_product in cart_products:
        product = db.get_product(product_id=cart_product.get('product_id'))
        order_id = cart_product.get('id')
        product_id = cart_product.get('product_id')
        quantity = cart_product.get('quantity')

        markup.row(
            InlineKeyboardButton(text=f"❌ {product.get('name')}",
                                 callback_data=f"overall-actions:delete:{order_id}:{product_id}:{quantity}")
        )
        markup.row(
            InlineKeyboardButton(text="-",
                                 callback_data=f"overall-actions:decrement:{order_id}:{product_id}:{quantity}"),
            InlineKeyboardButton(text=f"{quantity}",
                                 callback_data=f"overall-actions:show:{order_id}:{product_id}:{quantity}"),
            InlineKeyboardButton(text="+",
                                 callback_data=f"overall-actions:increment:{order_id}:{product_id}:{quantity}")
        )
    markup.row(
        InlineKeyboardButton(text=f"✅ Davom etish", callback_data=f"overall-actions:continue:{order_id}:{product_id}:{quantity}")
    )

    return markup.as_markup()
