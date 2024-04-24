import config

import asyncio
import telebot.async_telebot

bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'прив. я предложка для канала "Лук - рептилиям". теперь можно и от рептилий - Луку.\n'
                                'можешь написать /help для получения справки.')


@bot.message_handler(commands=['help'])
async def help_message(message):
    help_msg = """
    прив. я предложка для канала "Лук - рептилиям". теперь можно и от рептилий - Луку.
чтобы отправить что-либо в предложку, напиши /send. после этого я сообщу о готовности принять от тебя дары контента.
прошу заметить, что пост может быть отклонен по причинам, описанным и не описанным в уставе пивачка от 11.09.2021.
    """

    await bot.send_message(message.chat.id, help_msg)


@bot.message_handler(commands=['send'])
async def send_post(message):
    await bot.reply_to(message, 'чтобы отправить пост, *ответь мне на это сообщение* и вышли что угодно\. '
                                'после одобрения пост автоматически опубликуется мгновенно\.', parse_mode='MarkdownV2')


@bot.message_handler(commands=['approve'])
async def approve_post(message):
    if message.chat.id == config.ADMIN_CHAT_ID:
        await bot.send_message(message.chat.id, 'done.')
        await bot.copy_message(config.CHANNEL_ID, config.ADMIN_CHAT_ID, message.reply_to_message.message_id)
        await bot.send_message(message.reply_to_message.forward_origin.sender_user.id, 'пост опубликован.')
    else:
        await send_any(message)


@bot.message_handler(commands=['deny'])
async def deny_post(message):
    if message.chat.id == config.ADMIN_CHAT_ID:
        await bot.send_message(message.chat.id, 'нахуй!')
        await bot.send_message(message.reply_to_message.forward_origin.sender_user.id, 'пост твой отклонили.')
    else:
        await send_any(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'audio', 'document', 'photo', 'video'])
async def send_any(message):
    if not message.audio and not message.text and not message.document and not message.photo and not message.video:
        await bot.send_message(message.chat.id, 'какую-то херню ты мне подсунул, даже не буду отправлять это.')
        return

    if message.reply_to_message:
        if 'отправить' in message.reply_to_message.text and message.reply_to_message.from_user.is_bot:
            await bot.send_message(message.chat.id, 'отправил.')
            await bot.send_message(config.ADMIN_CHAT_ID, 'новая предложка:')
            await bot.forward_message(config.ADMIN_CHAT_ID, message.chat.id, message.message_id)

    else:
        await bot.send_message(message.chat.id, 'не понял, че ты там высрал, напиши /help, чтобы увидеть список '
                                                'доступных команд')


asyncio.run(bot.polling())
