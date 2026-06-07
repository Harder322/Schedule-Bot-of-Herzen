from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

inline_bt_cancel = InlineKeyboardButton(text='Отменить', callback_data='cancel')
inline_bt_confirm = InlineKeyboardButton(text='Подтвердить', callback_data='confirm')

inline_kb_confirm = InlineKeyboardMarkup(inline_keyboard=[[inline_bt_confirm, inline_bt_cancel]])


bt_back = KeyboardButton(text='◀ Назад')

bt_settings = KeyboardButton(text='⚙ Настройки')
bt_schedule_today = KeyboardButton(text='📗 Сегодня')
bt_schedule_tomorrow = KeyboardButton(text='📘 Завтра')
bt_schedule_curr_week = KeyboardButton(text='🔽 Эта неделя')
bt_schedule_next_week = KeyboardButton(text='▶ Следующая неделя')

kb_main = ReplyKeyboardMarkup(keyboard=[
    [bt_schedule_today, bt_schedule_tomorrow],
    [bt_schedule_curr_week, bt_schedule_next_week],
    [bt_settings]], resize_keyboard=True)

bt_mailing_config = KeyboardButton(text='✉ Настройка рассылки')
bt_group_config = KeyboardButton(text='🤓 Настройка группы')

inline_bt_unsub = InlineKeyboardButton(text='Отписаться от рассылки', callback_data='unsubscribe')

kb_settings = ReplyKeyboardMarkup(keyboard=[[bt_mailing_config], [bt_group_config], [bt_back]], resize_keyboard=True)

bt_admin_broadcast = KeyboardButton(text='✉ Отправить сообщение всем')
bt_admin_return = KeyboardButton(text='◀ Вернуть клавиатуру пользователя')

kb_admin = ReplyKeyboardMarkup(keyboard=[[bt_admin_broadcast], [bt_admin_return]], resize_keyboard=True)
