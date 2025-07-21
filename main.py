import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variabel global
waiting_users = []
matches = {}
blocked_users = set()
reports = set()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👋 Selamat datang di Anonymous Chat!\n"
        "Kirim /find untuk mulai mencari pasangan. \n"
        "Kirim /stop untuk keluar dari percakapan."
    )

async def find(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in matches:
        await update.message.reply_text("Kamu sedang dalam chat. Kirim /stop untuk keluar.")
        return
    if user_id in waiting_users:
        await update.message.reply_text("Sedang mencari pasangan. Tunggu sebentar...")
        return
    waiting_users.append(user_id)
    await update.message.reply_text("🔎 Sedang mencari pasangan...")
    if len(waiting_users) >= 2:
        user1 = waiting_users.pop(0)
        user2 = waiting_users.pop(0)
        matches[user1] = user2
        matches[user2] = user1
        try:
            await context.bot.send_message(chat_id=user1, text="🎉 Pasangan ditemukan! Mulai chatting.")
            await context.bot.send_message(chat_id=user2, text="🎉 Pasangan ditemukan! Mulai chatting.")
        except:
            pass

async def stop(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in matches:
        partner_id = matches.pop(user_id)
        matches.pop(partner_id, None)
        try:
            await context.bot.send_message(chat_id=partner_id, text="❗ Pasangan keluar dari chat.")
        except:
            pass
        await update.message.reply_text("🛑 Kamu keluar dari percakapan.")
        return
    if user_id in waiting_users:
        waiting_users.remove(user_id)
        await update.message.reply_text("🛑 Kamu berhenti mencari pasangan.")
        return
    await update.message.reply_text("Kamu tidak dalam percakapan atau mencari pasangan.")

async def message_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in matches:
        await update.message.reply_text("Ketik /find untuk mulai mencari pasangan.")
        return
    partner_id = matches[user_id]
    message_text = update.message.text
    try:
        await context.bot.send_message(chat_id=partner_id, text=message_text)
    except:
        await update.message.reply_text("Gagal mengirim pesan ke pasangan.")

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "/start - Penjelasan\n"
        "/find - Cari pasangan\n"
        "/stop - Keluar\n"
        "/block - Blokir\n"
        "/report - Lapor\n"
        "Kirim pesan untuk mengirim ke pasangan."
    )

async def block(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    blocked_users.add(user_id)
    if user_id in matches:
        partner_id = matches.pop(user_id)
        matches.pop(partner_id, None)
        try:
            await context.bot.send_message(chat_id=partner_id, text="❗ Kamu telah diblock dan keluar dari chat.")
        except:
            pass
    await update.message.reply_text("Kamu memblokir pengguna ini.")

async def report(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in matches:
        partner_id = matches.pop(user_id)
        matches.pop(partner_id, None)
        reports.add(partner_id)
        try:
            await context.bot.send_message(chat_id=partner_id, text="⚠️ Kamu dilaporkan dan keluar dari chat.")
        except:
            pass
        await update.message.reply_text("Pengguna dilaporkan dan keluar dari chat.")
    else:
        await update.message.reply_text("Kamu tidak dalam percakapan.")

async def main():
    TOKEN = os.environ.get("7825156787:AAE_P27gmb8LS0itkQQoqvCJv78i_HoPLsE")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('find', find))
    app.add_handler(CommandHandler('stop', stop))
    app.add_handler(CommandHandler('block', block))
    app.add_handler(CommandHandler('report', report))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    print("Bot berjalan...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
