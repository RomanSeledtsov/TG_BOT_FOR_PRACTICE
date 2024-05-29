from aiogram import Router, types
from aiogram.filters import Command

from config import bot, ADMIN_ID, MEDIA_PATH
from const import START_MENU_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    print(message)
    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,

        ),
        fetch='none'
    )
    photo_file = types.FSInputFile(MEDIA_PATH + "zaza.png")
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await start_menu_keyboard()
    )


@router.message(lambda message: message.text == "Kamada".lower())
async def admin_star_menu(message: types.Message,
                          db=AsyncDatabase()):
    if int(ADMIN_ID) == message.from_user.id:
        users = await db.execute_query(sql_queries.SELECT_USER_QUERY,
                                       fetch="all")
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Твоя панель админа 🫦"
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Пользователи бота 😢 {users} "
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="У тебя нет доступа козлина 😡"
        )
