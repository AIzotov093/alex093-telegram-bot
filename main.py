"""Main bot module for Alex093 Telegram Assistant.

Generates funny posts via GigaChat API using aiogram 3.x.
"""

import os
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp
import uuid
from base64 import b64encode
import random

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

GIGACHAT_AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
GIGACHAT_MODEL = "GigaChat"

class PostForm(StatesGroup):
    waiting_for_topic = State()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def generate_post_gigachat(prompt: str) -> Optional[str]:
    """Generate a funny post using GigaChat API."""
    try:
        auth_header = b64encode(
            f"{GIGACHAT_CLIENT_ID}:{GIGACHAT_CLIENT_SECRET}".encode()
        ).decode()
        
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {auth_header}"
        }
        
        token_data = {"scope": GIGACHAT_SCOPE}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GIGACHAT_AUTH_URL,
                headers=token_headers,
                data=token_data,
                ssl=False
            ) as token_response:
                if token_response.status != 200:
                    logger.error(f"Failed to get token: {token_response.status}")
                    return None
                
                token_resp_data = await token_response.json()
                access_token = token_resp_data.get("access_token")
                
                if not access_token:
                    logger.error("No access token in response")
                    return None
            
            chat_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            system_prompt = "Ты - веселый помощник. Генерируй смешные, остроумные и позитивные ответы."
            user_prompt = f"Сгенерируй шутливый ответ на запрос: {prompt}"
            
            chat_payload = {
                "model": GIGACHAT_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "update_interval": 0
            }
            
            async with session.post(
                GIGACHAT_API_URL,
                headers=chat_headers,
                json=chat_payload,
                ssl=False
            ) as chat_response:
                if chat_response.status != 200:
                    logger.error(f"Failed to get response: {chat_response.status}")
                    return None
                
                response_data = await chat_response.json()
                
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    message_content = response_data["choices"][0].get("message", {}).get("content", "")
                    return message_content
                
                return None
                
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

def format_post(content: str) -> str:
    """Format generated content with emoji, title and paragraphs."""
    emojis = ["✨", "🎉", "😄", "🚀", "💡", "🎯", "⭐", "🌟"]
    emoji = random.choice(emojis)
    
    post = f"{emoji} **Пост от Alex093**\n\n"
    post += f"{content}\n\n"
    post += f"{emoji} #AlexAssistant #Юмор"
    
    return post

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот Alex093. О чем поболтаем?")
    await state.set_state(PostForm.waiting_for_topic)

@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "Я - бот Alex093 для генерации смешных постов!\n\n"
        "Просто напишите мне тему или идею, и я сгенерирую для вас забавный пост.\n\n"
        "Команды:\n"
        "/start - Начать диалог\n"
        "/help - Помощь\n"
        "/cancel - Отменить текущую операцию"
    )
    await message.answer(help_text)

@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена. Можете начать заново с /start")

@dp.message(PostForm.waiting_for_topic)
async def process_topic(message: Message, state: FSMContext):
    topic = message.text
    await message.answer("⏳ Генерирую пост для вас...")
    
    post_content = await generate_post_gigachat(topic)
    
    if post_content:
        formatted_post = format_post(post_content)
        await message.answer(formatted_post, parse_mode="Markdown")
        await message.answer("Хотите еще один пост? Просто напишите новую тему!")
    else:
        await message.answer(
            "❌ Извините, не удалось сгенерировать пост. "
            "Пожалуйста, попробуйте позже или напишите другую тему."
        )
    
    await state.set_state(PostForm.waiting_for_topic)

@dp.message()
async def handle_text(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state == PostForm.waiting_for_topic:
        await process_topic(message, state)
    else:
        await state.set_state(PostForm.waiting_for_topic)
        await message.answer("Готов помочь! О чем вы хотите пост?")

async def main():
    try:
        logger.info("Starting bot Alex093...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env file")
        exit(1)
    
    if not GIGACHAT_CLIENT_ID or not GIGACHAT_CLIENT_SECRET:
        logger.error("GigaChat credentials not set in .env file")
        exit(1)
    
    asyncio.run(main())
