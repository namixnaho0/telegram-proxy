import asyncio
from telethon import TelegramClient, events

api_id = 34989957
api_hash = '667fedf082c996e42bf0840485f79582'
BOT_DESTINO = 'streamtestx3_bot'  # @streamtestx3_bot disney solamente
client = TelegramClient('session', api_id, api_hash)

client = TelegramClient('session', api_id, api_hash)

pendientes = {}

MENSAJE_AYUDA = """🤖 Bienvenido

Comandos disponibles:

/codedisney email@mail.com

Ejemplo:
/codedisney ejemplo@gmail.com
"""

#Ayuda al cliente baboso
@client.on(events.NewMessage(pattern=r'^/(start|help)$'))
async def ayuda(event):
    await event.reply(MENSAJE_AYUDA)

async def procesar(event, comando):
    texto = event.pattern_match.group(1)
    user_id = event.sender_id

    pendientes[user_id] = True

    await client.send_message(BOT_DESTINO, f"/{comando} {texto}")
    await event.reply(f"⏳ Procesando {comando}...")

@client.on(events.NewMessage(pattern=r'^/codedisney (.+)'))
async def code(event):
    await procesar(event, "code")

#RESPUESTA DEL BOT - forma por si tiene varias solicitudes 
@client.on(events.NewMessage(from_users=BOT_DESTINO))
async def respuesta(event):
    if pendientes:
        # Tomamos el primer usuario en espera
        user_id = list(pendientes.keys())[0]

        await client.send_message(user_id, f"📩 Resultado:\n{event.raw_text}")

        # Eliminamos usuario (ya atendido)
        pendientes.pop(user_id, None)

async def main():
    await client.start()
    print("✅ Script PRO encendido...")
    await client.run_until_disconnected()

asyncio.run(main())
