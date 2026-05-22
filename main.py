import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, BaseFilter
from aiohttp import web

TOKEN = "8884962646:AAHX5YyeLZ3yrKlJVzBSIUmkvUWd_kAyfRw"
TARGET_ID = 5560719948
TARGET_USERNAME = "nazik_maz1k"

logging.basicConfig(level=logging.WARNING)

bot = Bot(token=TOKEN)
dp = Dispatcher()
IS_FILTER_ENABLED = True

async def check_is_admin(message: types.Message, bot: Bot) -> bool:
    if message.chat.type == "private":
        return False
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False

class TargetUserFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        user = message.from_user
        if not user:
            return False
        return (user.id == TARGET_ID) or (user.username and user.username.lower() == TARGET_USERNAME)

@dp.message(Command("on"))
async def cmd_on(message: types.Message, bot: Bot):
    if not await check_is_admin(message, bot):
        return
    global IS_FILTER_ENABLED
    IS_FILTER_ENABLED = True
    await message.reply("допездівся дебіл соси хуяку")

@dp.message(Command("off"))
async def cmd_off(message: types.Message, bot: Bot):
    if not await check_is_admin(message, bot):
        return
    global IS_FILTER_ENABLED
    IS_FILTER_ENABLED = False
    await message.reply("хуй в презервативі говори")

@dp.message(TargetUserFilter())
async def delete_target_messages(message: types.Message):
    if not IS_FILTER_ENABLED:
        return
    try:
        await message.delete()
    except Exception:
        pass

# Заглушка для Render, щоб він думав, що це сайт і не вимикав бота
async def handle(request):
    return web.Response(text="Бот працює!")

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        pass
    
    # Запускаємо фоновий залінг бота
    asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    
    # Створюємо веб-сервер на порту, який вимагає Render
    app = web.Application()
    app.router.add_get('/', handle)
    
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    print("Веб-сервер заглушки запущено!")
    await site.start()
    
    # Тримаємо процес живим
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
