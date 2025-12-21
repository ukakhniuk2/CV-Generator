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
from discord.ext import commands
import json
from pathlib import Path

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True # Required for reading commands
bot = commands.Bot(command_prefix="/", intents=intents)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot.start(DISCORD_TOKEN))
    yield
    await bot.close()

app = FastAPI(lifespan=lifespan)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command(name="url_add")
async def url_add(ctx, url: str):
    json_path = Path(__file__).parent.parent / "urls.json"
    
    urls = []
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                urls = json.load(f)
        except json.JSONDecodeError:
            urls = []

    if url not in urls:
        urls.append(url)
        with open(json_path, 'w') as f:
            json.dump(urls, f, indent=4)
        await ctx.send(f"URL added: {url}")
    else:
        await ctx.send(f"URL already exists: {url}")

@bot.command(name="urls_show")
async def urls_show(ctx):
    json_path = Path(__file__).parent.parent / "urls.json"
    
    if not json_path.exists():
        await ctx.send("No URLs found. `urls.json` does not exist.")
        return

    try:
        with open(json_path, 'r') as f:
            urls = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        await ctx.send(f"Error reading `urls.json`: {e}")
        return

    if not urls:
        await ctx.send("The URL list is empty.")
        return

    message = "**Currently tracked URLs:**\n"
    for i, url in enumerate(urls, 1):
        line = f"{i}. {url}\n"
        if len(message) + len(line) > 1900:
            await ctx.send(message)
            message = ""
        message += line
    
    if message:
        await ctx.send(message)

@bot.command(name="url_remove")
async def url_remove(ctx, index: int):
    json_path = Path(__file__).parent.parent / "urls.json"
    
    if not json_path.exists():
        await ctx.send("No URLs found. `urls.json` does not exist.")
        return

    try:
        with open(json_path, 'r') as f:
            urls = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        await ctx.send(f"Error reading `urls.json`: {e}")
        return

    if not urls:
        await ctx.send("The URL list is empty.")
        return

    if index < 1 or index > len(urls):
        await ctx.send(f"Invalid index. Please provide a number between 1 and {len(urls)}.")
        return

    removed_url = urls.pop(index - 1)
    
    try:
        with open(json_path, 'w') as f:
            json.dump(urls, f, indent=4)
        await ctx.send(f"Removed URL: {removed_url}")
    except Exception as e:
        await ctx.send(f"Error saving `urls.json`: {e}")

@app.post("/notify")
async def notify_vacancy(vacancy: Vacancy, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_discord_message, vacancy)
    return {"status": "queued"}

async def send_discord_message(vacancy: Vacancy):
    await bot.wait_until_ready()
    
    try:
        channel = await bot.fetch_channel(int(CHANNEL_ID))
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

    # cover_letter_file = discord.File(io.StringIO(vacancy.cover_letter), filename="cover_letter.txt")
    # await channel.send(file=cover_letter_file)
    