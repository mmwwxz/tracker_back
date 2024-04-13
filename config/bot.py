import asyncio

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import *

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from config.tasks import send_telegram_notification

from decouple import config as conf

User = get_user_model()
bot_token = conf('BOT_TOKEN')
chat_id_admin = conf('CHAT_ID', cast=int)


@sync_to_async
def get_users():
    return list(
        User.objects.filter(subscription_start__isnull=False)
    )


async def start(update, context):
    await update.message.reply_text('Привет! Пожалуйста, отправьте ваш email для связи с аккаунтом.')


async def handle_message(update, context):
    chat_id = update.message.chat_id
    email = update.message.text
    if chat_id == chat_id_admin:
        text = update.message.text
        users = await get_users()
        [send_telegram_notification(user.telegram_chat_id, text) for user in users]
        await update.message.reply_text(f'Вы успешно разослали уведомление: {text} всем пользователям!')
    else:
        try:
            user = await sync_to_async(User.objects.get)(telegram_chat_id=chat_id)
            await update.message.reply_text('Вы уже связали эл. почту к своему аккаунту!')
        except:
            try:
                user = await sync_to_async(User.objects.get)(email=email)
                user.telegram_chat_id = chat_id
                await sync_to_async(user.save)()
                await update.message.reply_text(f'{user.username}, ваш Telegram ID успешно связан с вашим аккаунтом.\nПриятной работы!')
            except User.DoesNotExist:
                await update.message.reply_text('Аккаунт с таким email не найден.')


def main():
    application = Application.builder().token(bot_token).build()

    start_button = KeyboardButton('/startup steps')
    start_kb = ReplyKeyboardMarkup([[start_button]], resize_keyboard=True, one_time_keyboard=True)

    application.add_handler(CommandHandler('startup steps', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(MessageHandler(filters.COMMAND, lambda u, c: u.message.reply_text("Добро пожаловать!",
                                                                                              reply_markup=start_kb)))

    application.run_polling()


if __name__ == '__main__':
    main()
