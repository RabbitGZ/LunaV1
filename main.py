import discord
import os
from groq import Groq

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client_ai = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Eres un bot de Discord amable, divertido y que responde en español.
Respuestas cortas, naturales y útiles.
"""

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    response = client_ai.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.content}
        ]
    )

    await message.channel.send(response.choices[0].message.content)

bot.run(DISCORD_TOKEN)
