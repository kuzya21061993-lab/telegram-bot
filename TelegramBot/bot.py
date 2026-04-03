import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = "8765263256:AAElamGLZqBAVyuc6WdqNfwCoZuvpKqU8fc"
OWNER_ID = 5428973280

bot = Bot(token=TOKEN)
dp = Dispatcher()

BAD_WORDS = [
    "продаю",
    "акція",
    "спам",
    "послуги",
    "пропоную послуги",
    "запрошення в групу",
    "продам",
    "продаж",
    "реклама",
    "ціна в лс",
    "опт",
    "продам дешево",
    "акція"
]
RULES_TEXT = (
    "🚫 Увага! Безкоштовна реклама в цій групі заборонена.\n"
    "Якщо хочеш розмістити рекламу, звертайся до адміністраторів групи.\n"
    "Лише платна реклама можлива — безкоштовна видаляється та за неї можна отримати бан.\n"
    "Дякуємо за розуміння! ✅" )


# 🔑 Перевірка: адмін чи ні
async def is_admin(message: Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["administrator", "creator"]

@dp.message()
async def anti_spam(message: Message):
    if not message.text:
        return

    text = message.text.lower()

    if any(word in text for word in BAD_WORDS):

        # ✅ Якщо адмін або власник — пропускаємо
        if await is_admin(message) or message.from_user.id == OWNER_ID:
            return

        user = message.from_user

        # 🧹 Видалити повідомлення
        try:
            await message.delete()
        except:
            pass

        # ⚠️ Попередження
        try:
            await message.answer(RULES_TEXT)
        except:
            pass

        # 📩 Повідомлення власнику
        try:
            await bot.send_message(
                OWNER_ID,
                f"🚨 СПАМ!\n\n"
                f"👤 {user.full_name}\n"
                f"🆔 {user.id}\n"
                f"💬 {message.text}"
            )
        except:
            pass


async def main():
    print("🤖 Бот працює...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())