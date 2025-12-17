import discord
import io
from generator.latex_to_pdf import compile_latex_to_pdf
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import os
from contextlib import asynccontextmanager
from collector.models import Vacancy
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
async def notify_vacancy(vacancy: Vacancy, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_discord_message, vacancy)
    return {"status": "queued"}

async def send_discord_message(vacancy: Vacancy):
    await client.wait_until_ready()
    
    try:
        channel = await client.fetch_channel(int(CHANNEL_ID))
    except discord.NotFound:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")
        return
    except discord.Forbidden:
        print(f"Error: Bot does not have permission to access channel {CHANNEL_ID}.")
        return
    except Exception as e:
        print(f"Error fetching channel: {e}")
        return
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
        f"**Description:** {vacancy.description[:1000] + '...' if vacancy.description and len(vacancy.description) > 1000 else vacancy.description}\n"
    )
    if len(message) > 2000:
        message = message[:1990] + "..."
    await channel.send(message)

    pdf_bytes = await asyncio.to_thread(compile_latex_to_pdf, vacancy.cv_code)
    pdf_file = discord.File(io.BytesIO(pdf_bytes), filename="cv.pdf")
    await channel.send(file=pdf_file)

    txt_file = discord.File(io.StringIO(vacancy.cv_code), filename="latex_code.txt")
    await channel.send(file=txt_file)
