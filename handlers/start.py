from aiogram import types
from aiogram.filters.command import CommandStart

from keyboards.reply.main_menu import generate_main_menu
from loader import db
from router import router


@router.message(CommandStart())
async def start(message: types.Message):
    try:
        db.register_user(message.from_user.id,
                         message.from_user.full_name,
                         message.from_user.username)
        await message.answer("Assalomu alaykum, muvaffaqiyatli ro'yxatga olindingiz!",
                             reply_markup=generate_main_menu())
    except:
        await message.answer("Xush kelibsiz, qaytganingizdan xursandmiz!", reply_markup=generate_main_menu())
