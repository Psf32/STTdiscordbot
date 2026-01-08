import discord
from discord import app_commands
from discord.ext import commands, voice_recv
import os
from dotenv import load_dotenv
from google.cloud import speech
import io

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_CREDS = os.getenv('GOOGLE_CLOUD')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Started: {self.user}")

bot = MyBot()

@bot.tree.command(name="join", description="Join VC to listen")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect(cls=voice_recv.VoiceRecvClient)
        await interaction.response.send_message(f"Connected to {channel.mention}.")
    else:
        await interaction.response.send_message("Join a VC first!", ephemeral=True)

@bot.tree.command(name="record", description="Start recording audio")
async def record(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc:
        return await interaction.response.send_message("I'm not in a VC.")
    
    vc.listen(voice_recv.WaveSink("session.wav"))
    await interaction.response.send_message("listening...)")

@bot.tree.command(name="stop", description="Stop and Transcribe")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_listening():
        await interaction.response.defer()
        vc.stop_listening()

        try:
            client = speech.SpeechClient.from_service_account_file(GOOGLE_CREDS)
            
            with io.open("session.wav", "rb") as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=48000,
                language_code="en-US",
                audio_channel_count=2,
                enable_automatic_punctuation=True,
            )

            response = client.recognize(config=config, audio=audio)
            
            final_transcript = ""
            for result in response.results:
                final_transcript += result.alternatives[0].transcript + "\n"

            if not final_transcript:
                final_transcript = "[No speech detected or audio was too quiet]"

            word_count = len(final_transcript.split())
            filename = "transcript.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"TRANSCRIPT\n")
                f.write(f"Words: {word_count}\n")
                f.write(f"-------------------------------\n\n")
                f.write(final_transcript)
            
            await interaction.followup.send(
                f"Transcription Complete\nTotal Words: {word_count}",
                file=discord.File(filename)
            )

        except Exception as e:
            await interaction.followup.send(f"Google Cloud Error: {e}")

    else:
        await interaction.response.send_message("I wasn't recording.")

@bot.tree.command(name="leave", description="Disconnect")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Disconnected.")

if __name__ == "__main__":
    bot.run(TOKEN)