import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@earnhubnr"


FORCE_JOIN_TEXT = """
🌟 Welcome to EARN HUB NR! 🌟

🚀 বটটি ব্যবহার করার আগে আমাদের Official Channel-এ Join করা বাধ্যতামূলক।

📢 Channel-এ Join করে নিচের “✅ CHECK JOINED” বাটনে ক্লিক করুন।

💙 আমাদের সাথে থাকুন এবং সব নতুন Update সবার আগে পান!
"""


def force_join_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 JOIN CHANNEL",
                url="https://t.me/earnhubnr"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ CHECK JOINED",
                callback_data="check_join"
            )
        ]
    ])


async def is_joined(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        return member.status in ["member", "administrator", "creator"]

    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if await is_joined(user_id, context):
        await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            FORCE_JOIN_TEXT,
            reply_markup=force_join_keyboard()
        )


async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_joined(user_id, context):

        await query.edit_message_text(
            "🎉 সফলভাবে Channel Join করেছেন!\n\n"
            "✅ এখন আপনি EARN HUB NR ব্যবহার করতে পারবেন।"
        )

        await show_main_menu(query, context)

    else:

        await query.answer(
            "❌ আপনি এখনো Channel Join করেননি!",
            show_alert=True
        )


async def show_main_menu(update, context):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 ACCOUNT", callback_data="account"),
            InlineKeyboardButton("💰 BALANCE", callback_data="balance")
        ],
        [
            InlineKeyboardButton("👥 REFERRALS", callback_data="referrals"),
            InlineKeyboardButton("💸 WITHDRAW", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("📢 NOTICE", callback_data="notice"),
            InlineKeyboardButton("❓ HELP", callback_data="help")
        ]
    ])

    text = """
🎉 Welcome to EARN HUB NR!

আপনি সফলভাবে Channel Join করেছেন।

নিচের Menu থেকে আপনার প্রয়োজনীয় Option নির্বাচন করুন 👇
"""

    if hasattr(update, "message") and update.message:
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "account":
        await query.message.reply_text(
            "👤 ACCOUNT\n\n"
            "এই অংশটি পরে তোমার প্রয়োজন অনুযায়ী তৈরি করা যাবে।"
        )

    elif query.data == "balance":
        await query.message.reply_text(
            "💰 BALANCE\n\n"
            "Database ছাড়া Balance স্থায়ীভাবে সংরক্ষণ করা যাবে না।"
        )

    elif query.data == "referrals":
        await query.message.reply_text(
            "👥 REFERRALS\n\n"
            "Referral system যোগ করতে চাইলে পরবর্তীতে database/storage লাগবে।"
        )

    elif query.data == "withdraw":
        await query.message.reply_text(
            "💸 WITHDRAW\n\n"
            "Withdrawal system পরবর্তীতে যোগ করা যাবে।"
        )

    elif query.data == "notice":
        await query.message.reply_text(
            "📢 NOTICE\n\n"
            "কোনো নতুন Notice নেই।"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "❓ HELP\n\n"
            "যেকোনো সমস্যায় Admin-এর সাথে যোগাযোগ করুন।"
        )


def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable পাওয়া যায়নি!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_joined, pattern="^check_join$"))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("EARN HUB NR Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
