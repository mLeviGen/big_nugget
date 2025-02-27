from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.types import (
    FSInputFile,
    InputMediaPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from app.settings.config import *
from app.funcs import get_username
import logging

router = Router()
image_main = FSInputFile("app/images/menus/nugget.png")


def set_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗺️ Карта", callback_data=f"show_map_{user_id}")],
            [
                InlineKeyboardButton(
                    text="🚨 Тривога", callback_data=f"check_alert_{user_id}"
                )
            ],
        ]
    )


async def show_main_menu(bot, chat_id, user_id):
    username = await get_username(user_id)
    try:
        await bot.send_photo(
            chat_id,
            image_main,
            caption=CAPTION.format(username),
            reply_markup=set_keyboard(user_id),
        )
    except Exception as e:
        logging.error(f"Помилка відправлення головного меню: {e}")


@router.message(Command(commands=["menu"]))
async def show_menu(message: types.Message, bot: Bot):
    await show_main_menu(bot, message.chat.id, message.from_user.id)


@router.message(Command(commands=["start"]))
async def show_menu(message: types.Message, bot: Bot):
    await show_main_menu(bot, message.chat.id, message.from_user.id)


@router.callback_query(lambda c: c.data.startswith("back_to_menu_"))
async def handle_back_to_menu(callback_query: types.CallbackQuery, bot: Bot):
    user_id = int(callback_query.data.split("_")[-1])
    username = await get_username(user_id)

    if callback_query.from_user.id != user_id:
        await callback_query.answer(BAD_ANSWER, show_alert=True)
        return

    try:
        media = InputMediaPhoto(
            media=image_main,
            caption=CAPTION.format(username),
        )
        await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=media,
            reply_markup=set_keyboard(user_id),
        )
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Помилка відправлення головного меню: {e}")
        await callback_query.answer("Помилка відправлення головного меню.")
