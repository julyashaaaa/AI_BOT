import aiogram
import os
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import requests
import json
router = Router()
messages = {}

TOKEN = os.getenv("7477662057:AAGANBOyg1sgf_-GM1LAiPiLESGJSj4g5-U")  # Токен вашего Telegram-бота
LLM_TOKEN = os.getenv("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")  # Токен для доступа к LLM API


def get_response(messages):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ.get('LLM_TOKEN')}"
    },
    data=json.dumps({
        "model": "openai/gpt-4o-mini",
        "messages": messages
    })
    )

    return response.json()['choices'][0]['message']['content']



@router.message()
async def message_handler(msg):
    if msg.chat.id not in messages.keys():
        messages[msg.chat.id] = []

    if msg.text is None:
        return await msg.answer("Извини, но я пока принимаю только текст!")


    messages[msg.chat.id].append({'role': 'user', 'content': msg.text})
    response = get_response(messages[msg.chat.id])
    await msg.answer(response, parse_mode=ParseMode.MARKDOWN)
@router.message(CommandStart())
async def start(msg):
    await msg.mark("Привет, я бот для взаимодействия с LLM!")
@router.message(Command("help"))
async def help(msg):
    await msg.answer("Можешь написать мне сообщение, а я постараюсь вам на него ответить!")

async def main():
    bot = aiogram.Bot(os.environ.get("TOKEN") )

    dp = aiogram.Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())