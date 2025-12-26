# Job Vacancy Notifier & CV Adapter Bot

This application monitors job vacancies on JustJoin.it, automatically generates a tailored CV using OpenAI (GPT), converts it to PDF (LaTeX), and notifies you via Discord.

## Features
- **Job Scraping**: Monitors specific job filters on JustJoin.it.
- **AI CV Adaptation**: Uses OpenAI to adapt your CV for each specific job description.
- **PDF Generation**: Converts the adapted CV from LaTeX to PDF.
- **Discord Notifications**: Sends the vacancy details and the generated PDF CV directly to your Discord channel.
- **Dockerized**: easy to deploy and run anywhere.

## Prerequisites
- **Docker** and **Docker Compose** installed.
- **OpenAI API Key**.
- **Discord Bot Token** and **Channel ID**.

## Setup & Deployment

### 1. Clone the repository
```bash
git clone <repository_url>
cd bot7
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory. You can use `.env.example` as a template:
```bash
cp .env.example .env
```
Edit `.env` and fill in your secrets:
```ini
DISCORD_BOT_TOKEN=your_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
OPENAI_API_KEY=sk-your_openai_key_here
BOT_URL=http://bot:8000
```

### 3. Run with Docker Compose
To build and start the application in the background:
```bash
docker-compose up -d --build
```
*Note: The first build may take a few minutes because it installs full LaTeX support.*

### 4. Update & Redeploy
If you pull new changes from git, simply run:
```bash
git pull
docker-compose up -d --build
```

## Project Structure
- `app/`: Main parser logic.
- `bot/`: FastAPI server and Discord bot.
- `collector/`: Functions for job vacancy parsing.
- `generator/`: Logic for CV generation (OpenAI) and PDF conversion (LaTeX).
- `database/`: SQLite database storage.

## Troubleshooting
- **Logs**: Check logs with `docker-compose logs -f`.
- **DNS Issues**: The parser is configured to use Google DNS (8.8.8.8) to prevent resolution errors in Docker.
