from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot, ADMIN_ID, MEDIA_PATH
from const import START_MENU_TEXT, PROFILE_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard

router = Router()


class RegistrationStates(StatesGroup):
    nickname = State()
    bio = State()
    gender = State()
    birthday = State()
    photo = State()


@router.callback_query(lambda call: call.data == "registration")
async def registration_start(call: types.CallbackQuery,
                             state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Придумай себе никнейм 🤖 "
    )
    await state.set_state(RegistrationStates.nickname)


@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Чем увлекаешься ? 🥱"
    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.bio)


@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message, state: FSMContext):
    await state.update_data(bio=message.text)
    # await bot.send_message(
    #     chat_id=message.from_user.id,
    #     text="Твой пол ?"
    # )
    # data = await state.get_data()
    # print(data)
#     await state.set_state(RegistrationStates.gender)
#
#
# @router.message(RegistrationStates.gender)
# async def process_bio(message: types.Message, state: FSMContext):
#     await state.update_data(gender=message.text)
#     await bot.send_message(
#         chat_id=message.from_user.id,
#         text=""
#     )
#     await state.set_state(RegistrationStates.birthday)


# @router.message(RegistrationStates.birthday)
# async def process_bio(message: types.Message, state: FSMContext):
#     await state.update_data(birthday=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Пришли свое фото 👀"
    )
    await state.set_state(RegistrationStates.photo)


@router.message(RegistrationStates.photo)
async def process_photo(message: types.Message,
                        state: FSMContext,
                        db=AsyncDatabase,):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    media_final_path = 'media/' + file_path
    await bot.download_file(
        file_path,
        'media/' + file_path
    )
    data = await state.get_data()

    photo = FSInputFile('media/' + file_path)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=data['nickname'],
            bio=data['bio'],
        )
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Вы успешно зарегистрировались 🎉 "
    )



