import asyncio
from datetime import timedelta
import logging

from aiogram import types, F, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from scripts.bot import dp, db, bot

from data.config import ADMIN_TELEGRAM_ID
from scripts import keyboards
from scripts.states import Broadcast, BroadcastAbort
from scripts.message_handlers import broadcast_message


@dp.message(F.from_user.id == ADMIN_TELEGRAM_ID, Command('admin'))
async def show_admin_menu(msg: Message):
    await msg.answer("Привет, админ!", reply_markup=keyboards.kb_admin)


@dp.message(F.from_user.id == ADMIN_TELEGRAM_ID, F.text == keyboards.bt_admin_return.text)
async def show_admin_menu(msg: Message):
    await msg.answer("Пока, админ!", reply_markup=keyboards.kb_main)


@dp.message(F.from_user.id == ADMIN_TELEGRAM_ID, F.text == keyboards.bt_admin_broadcast.text)
async def get_broadcast_message(msg: types.Message, state: FSMContext):
    await msg.answer("Пришлите сообщение, которое нужно разослать всем пользователям...")
    await state.set_state(Broadcast.Message)


@dp.message(F.from_user.id == ADMIN_TELEGRAM_ID, Broadcast.Message)
async def confirm_broadcast_message(msg: types.Message, state: FSMContext):
    await state.update_data(message=msg)

    await msg.forward(ADMIN_TELEGRAM_ID)
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Переслать', callback_data='forward'))
    builder.add(InlineKeyboardButton(text='Отправить копию', callback_data='copy'))
    builder.row(keyboards.inline_bt_cancel)
    
    await msg.answer("Вы хотите переслать сообщение или отправить копию от имени бота?",
                        reply_markup=builder.as_markup())
    await state.set_state(Broadcast.MessageType)


@dp.callback_query(F.from_user.id == ADMIN_TELEGRAM_ID, Broadcast.MessageType)
async def send_broadcast_message(call: CallbackQuery, state: FSMContext):
    await call.answer()
    
    data = await state.get_data()
    msg = data['message']
    msg_type = call.data
    await state.clear()

    all_id = db.get_all_id()
    all_id.remove((ADMIN_TELEGRAM_ID,))

    max_counter = len(all_id)
    update_interval = max(1, max_counter // 100)  # Update every 1% or at least every user if less than 100 users

    await call.bot.send_message(ADMIN_TELEGRAM_ID, f"Это займет примерно {timedelta(seconds=max_counter * 0.5)}.")
    await call.message.edit_text(f"Хорошо, отправляю {max_counter} сообщений...",
                                    reply_markup=InlineKeyboardMarkup(
                                        inline_keyboard=[[InlineKeyboardButton(
                                            text="Отменить", callback_data="abort_broadcast")]]))

    for msg_counter, user_id in enumerate(all_id, start=1):
        # Check if the broadcast has been aborted
        if await state.get_state() == BroadcastAbort.Abort:
            text = f"🚫 Рассылка отменена. Отправлено {msg_counter - 1} из {max_counter}."
            await call.message.edit_text(text)
            break

        await broadcast_message(user_id[0], msg, msg_type)
        
        if msg_counter % update_interval == 0 or msg_counter == max_counter:
            progress = (msg_counter / max_counter) * 100
            progress_bar = f"<code>[{'#' * (int(progress) // 5)}{'-' * (20 - (int(progress) // 5))}]</code>"
            await call.message.edit_text(f"Отправлено {msg_counter} из {max_counter} ({progress:.2f}%) {progress_bar}",
                                            reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                                [[InlineKeyboardButton(text="Отменить", callback_data="abort_broadcast")]]))
        
        await asyncio.sleep(.5)


@dp.callback_query(F.from_user.id == ADMIN_TELEGRAM_ID, F.data == "abort_broadcast")
async def abort_broadcast(call: CallbackQuery, state: FSMContext):
    await state.set_state(BroadcastAbort.Abort)
    await call.answer("Рассылка будет отменена.")


