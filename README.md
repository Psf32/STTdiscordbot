# Discord Voice Transcription Bot

A Discord bot that joins voice channels, records audio, and transcribes speech using Google Cloud Speech-to-Text. Designed to be reliable for longer voice sessions and multi-server use.

## Features
- Slash commands: `/join`, `/record`, `/stop`, `/leave`
- Records Discord voice channels to WAV files (16-bit PCM)
- Automatically detects audio parameters (sample rate, channels)
- Uses Google Cloud long-running recognition for longer audio
- Per-guild audio and transcript isolation
- Cleans up temporary audio and transcript files after use

## Commands
| Command | Description |
|--------:|-------------|
| `/join` | Join the user’s current voice channel |
| `/record` | Start recording voice audio |
| `/stop` | Stop recording and transcribe audio |
| `/leave` | Disconnect from the voice channel |

## Tech stack
- Python 3.10+
- discord.py (app commands / slash commands)
- discord-ext-voice-recv
- Google Cloud Speech-to-Text
- asyncio for non-blocking transcription

## Setup

1. Clone the repository
```bash
git clone https://github.com/psf32/discord-voice-transcriber.git
cd discord-voice-transcriber
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Environment variables

Create a `.env` file in the project root with the following keys:
```env
DISCORD_TOKEN=your_discord_bot_token
GOOGLE_CLOUD=/absolute/path/to/service_account.json
```
⚠️ `GOOGLE_CLOUD` must be a path to a service account JSON file (the file path), not the JSON contents.

## Google Cloud setup
1. Create a Google Cloud project (or use an existing one).  
2. Enable the Speech-to-Text API for the project.  
3. Create a service account with the necessary permissions for Speech-to-Text.  
4. Download the service account JSON key file.  
5. Store the JSON file locally and set the `GOOGLE_CLOUD` path in your `.env`.

## Running the bot
Start the bot:
```bash
python bot.py
```
Then:
1. Invite the bot to your server.  
2. Join a voice channel.  
3. Use `/join`, then `/record`. Speak while recording.  
4. Use `/stop` to end recording and receive a transcript file.

## Notes & limitations
- Audio is recorded and transcribed after stopping — not real-time transcription.
- Audio must be 16-bit PCM WAV (the sink handles conversion automatically).
- Accuracy depends on Discord audio quality and background noise.
- Intended for educational / personal use.

## Contributing
Issues and pull requests welcome. Please follow standard contribution etiquette.

## License
Specify your license here (e.g., MIT) or add a LICENSE file to the repository.
Designed for educational / personal use
