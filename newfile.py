import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, BaseFilter

TOKEN="8884962646:AAHX5YyeLZ3yrKlJVzBSIUmkvUWd_kAyfRw"
TARGET_ID = 5560719948
TARGET_USERNAME = "Nazik_Maz1k"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Глобальна змінна для зберігання стану (True - видаляємо, False - ігноруємо)
# За замовчуванням система увімкнена
IS_FILTER_ENABLED = True

# Фільтр для перевірки, чи є користувач адміністратором чату
class IsAdminFilter(BaseFilter):
    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        if message.chat.type in ["private"]:
            return False
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return member.status in ["administrator", "creator"]

# Фільтр для виявлення "цільового" користувача
class TargetUserFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if not message.from_user:
            return False
        is_target_id = message.from_user.id == TARGET_ID
        is_target_username = message.from_user.username and message.from_user.username.lower() == TARGET_USERNAME.lower()
        return is_target_id or is_target_username


# Команда увімкнення (доступна тільки адмінам)
@dp.message(Command("on"), IsAdminFilter())
async def cmd_on(message: types.Message):
    global IS_FILTER_ENABLED
    IS_FILTER_ENABLED = True
    await message.reply("Автовидалення повідомлень від хуяковського хай йде нахуй деган **УВІМКНЕНО**.")

# Команда вимкнення (доступна тільки адмінам)
@dp.message(Command("off"), IsAdminFilter())
async def cmd_off(message: types.Message):
    global IS_FILTER_ENABLED
    IS_FILTER_ENABLED = False
    await message.reply("Автовидалення повідомлень дебіл най піздить **ВИМКНЕНО**.")


# Хендлер видалення (спрацює, тільки якщо фільтрація активна)
@dp.message(TargetUserFilter())
async def delete_target_messages(message: types.Message):
    global IS_FILTER_ENABLED
    if not IS_FILTER_ENABLED:
        return  # Якщо вимкнено, просто ігноруємо
        
    try:
        await message.delete()
        logging.info(f"Видалено повідомлення від {message.from_user.id}")
    except Exception as e:
        logging.error(f"Помилка видалення: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
