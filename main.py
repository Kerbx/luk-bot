import config

import asyncio
import telebot.async_telebot

bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def send_start(message):
    await bot.reply_to(message, 'прив\. '
                                'я предложка для канала "Лук \- рептилиям"\. теперь можно и от рептилий \- Луку\.\n'
                                'можешь написать /help для получения справки\.', parse_mode='MarkdownV2')


@bot.message_handler(commands=['help'])
async def help_message(message):
    help_msg = """
    прив\.\nя предложка для канала "Лук \- рептилиям"\. теперь можно и от рептилий \- Луку\.
чтобы отправить что\-либо в предложку, напиши /send\. после этого я сообщу о готовности принять от тебя дары контента\.
прошу заметить, что пост может быть отклонен по причинам, описанным и не описанным в уставе пивачка от 11\.09\.2021\.
    """

    await bot.send_message(message.chat.id, help_msg, parse_mode='MarkdownV2')


@bot.message_handler(commands=['send'])
async def send_post(message):
    await bot.reply_to(message, 'чтобы отправить пост, *ответь мне на это сообщение* и вышли что угодно\. '
                                'после одобрения пост автоматически опубликуется мгновенно\.', parse_mode='MarkdownV2')


@bot.message_handler(commands=['approve'])
async def approve_post(message):
    if message.chat.id == config.ADMIN_CHAT_ID:
        new_message = message.reply_to_message
        new_message.text = telebot.formatting.escape_markdown(new_message.text)
        new_message.text += '\n\n[отправлено из предложки\.](tg://user?id=7143585636)'
        new_message_id = await bot.send_message(message.chat.id, new_message.text, parse_mode='MarkdownV2')
        new_message_id = new_message_id.message_id

        await bot.copy_message(config.CHANNEL_ID, config.ADMIN_CHAT_ID, new_message_id, parse_mode='MarkdownV2')
        await bot.delete_message(message.chat.id, message.message_id - 2)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, new_message_id)
        await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        await bot.send_message(message.chat.id, 'done\.', parse_mode='MarkdownV2')
        await bot.send_message(message.reply_to_message.forward_origin.sender_user.id, '_пост опубликован\._',
                               parse_mode='MarkdownV2')
    else:
        await send_any(message)


@bot.message_handler(commands=['deny'])
async def deny_post(message):
    if message.chat.id == config.ADMIN_CHAT_ID:
        await bot.send_message(message.chat.id, 'нахуй\!', parse_mode='MarkdownV2')
        await bot.send_message(message.reply_to_message.forward_origin.sender_user.id, 'пост твой отклонили\.',
                               parse_mode='MarkdownV2')
    else:
        await send_any(message)


@bot.message_handler(func=lambda message: True, content_types=['text', 'audio', 'document', 'photo', 'video'])
async def send_any(message):
    if not message.audio and not message.text and not message.document and not message.photo and not message.video:
        await bot.send_message(message.chat.id, 'какую\-то херню ты мне подсунул, даже не буду отправлять это\.',
                               parse_mode='MarkdownV2')
        return

    if message.reply_to_message:
        if 'отправить' in message.reply_to_message.text and message.reply_to_message.from_user.is_bot:
            await bot.send_message(message.chat.id, 'отправил\.', parse_mode='MarkdownV2')
            await bot.send_message(config.ADMIN_CHAT_ID, 'новая предложка:', parse_mode='MarkdownV2')
            await bot.forward_message(config.ADMIN_CHAT_ID, message.chat.id, message.message_id)
    elif 'гойда' in message.text.lower():
        await bot.send_message(message.chat.id, 'наш слон\!\n*ГОЙДА\!*', parse_mode='MarkdownV2')
    else:
        await bot.send_message(message.chat.id, 'не понял, че ты там высрал, напиши /help, чтобы увидеть список '
                                                'доступных команд\.', parse_mode='MarkdownV2')


asyncio.run(bot.polling())
