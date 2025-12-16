import discord
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import os
from contextlib import asynccontextmanager
from collector.models import JustJoinItVacancy
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(client.start(DISCORD_TOKEN))
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@app.post("/notify")
async def notify_vacancy(vacancy: JustJoinItVacancy, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_discord_message, vacancy)
    return {"status": "queued"}

async def send_discord_message(vacancy: JustJoinItVacancy):
    await client.wait_until_ready()
    
    channel = client.get_channel(int(CHANNEL_ID))
    message = (
        f"**New Job Found!**\n"
        f"**Link:** {vacancy.link}\n"
        f"**Title:** {vacancy.title}\n"
        f"**Company:** {vacancy.company}\n"
        f"**Location:** {vacancy.location}\n"
        f"**Salary:** {vacancy.salary}\n"
        f"**Cards:** {vacancy.cards}\n"
        f"**Is Remote:** {vacancy.is_remote}\n"
        f"**Is One Click:** {vacancy.is_one_click}\n"
        f"**Description:** {vacancy.description}\n"
    )
    await channel.send(message)

    file = discord.File(io.StringIO(vacancy.cv_code), filename="cv.txt")
    await channel.send(file=file)
