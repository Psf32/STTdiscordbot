Discord Voice Transcription Bot

A Discord bot that joins voice channels, records audio, and transcribes speech using Google Cloud Speech-to-Text.
Designed to be reliable for longer voice sessions and multi-server use.

Features

Slash commands (/join, /record, /stop, /leave)

Records Discord voice channels to WAV files

Automatically detects audio parameters (sample rate, channels)

Uses Google Cloud long-running recognition for longer audio

Per-guild audio and transcript isolation

Cleans up temporary audio and transcript files after use

Commands
Command	Description
/join	Join the user’s current voice channel
/record	Start recording voice audio
/stop	Stop recording and transcribe audio
/leave	Disconnect from the voice channel
Tech Stack

Python 3.10+

discord.py (app commands/slash commands)

discord-ext-voice-recv

Google Cloud Speech-to-Text

asyncio for non-blocking transcription

Setup
1. Clone the repository
git clone https://github.com/psf32/discord-voice-transcriber.git
cd discord-voice-transcriber

2. Install dependencies
pip install -r requirements.txt

3. Environment variables

Create a .env file:

DISCORD_TOKEN=your_discord_bot_token
GOOGLE_CLOUD=/absolute/path/to/service_account.json


⚠️ GOOGLE_CLOUD must be a path to a service account JSON file, not the JSON contents.

Google Cloud Setup

Create a Google Cloud project

Enable Speech-to-Text API

Create a service account

Download the service account JSON key

Set the JSON file path in .env

Running the Bot

Run bot.py in the Python console
python bot.py


Once running:

Invite the bot to your server

Join a voice channel

Use /join, then /record

Speak

Use /stop to receive a transcript file

Notes & Limitations

Audio must be 16-bit PCM WAV (handled automatically by the sink)

Accuracy depends on Discord audio quality and background noise

Not real-time transcription (post-processing after /stop)

Designed for educational / personal use
