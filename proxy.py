import asyncio
from telethon import TelegramClient, events

api_id = 34989957
api_hash = '667fedf082c996e42bf0840485f79582'
BOT_DESTINO = 'miembroextrabot'  # sin @
client = TelegramClient('session', api_id, api_hash)

client = TelegramClient('session', api_id, api_hash)

# 🔥 Diccionario para manejar usuarios correctamente
pendientes = {}

# 📌 MENSAJE DE AYUDA
MENSAJE_AYUDA = """🤖 Bienvenido

Comandos disponibles:

/code correo
/link correo
/activarTV correo

Ejemplo:
/code ejemplo@gmail.com
"""

# 🟢 HELP
@client.on(events.NewMessage(pattern=r'^/(start|help)$'))
async def ayuda(event):
    await event.reply(MENSAJE_AYUDA)

# 🔧 Función general para enviar comandos
async def procesar(event, comando):
    texto = event.pattern_match.group(1)
    user_id = event.sender_id

    # Guardamos usuario con el comando que pidió
    pendientes[user_id] = True

    await client.send_message(BOT_DESTINO, f"/{comando} {texto}")
    await event.reply(f"⏳ Procesando {comando}...")

# 🟢 /code
@client.on(events.NewMessage(pattern=r'^/code (.+)'))
async def code(event):
    await procesar(event, "code")

# 🟢 /link
@client.on(events.NewMessage(pattern=r'^/link (.+)'))
async def link(event):
    await procesar(event, "link")

# 🟢 /activarTV
@client.on(events.NewMessage(pattern=r'^/activarTV (.+)'))
async def tv(event):
    await procesar(event, "activarTV")

# 🟢 RESPUESTA DEL BOT
@client.on(events.NewMessage(from_users=BOT_DESTINO))
async def respuesta(event):
    if pendientes:
        # Tomamos el primer usuario en espera
        user_id = list(pendientes.keys())[0]

        await client.send_message(user_id, f"📩 Resultado:\n{event.raw_text}")

        # Eliminamos ese usuario (ya atendido)
        pendientes.pop(user_id, None)

async def main():
    await client.start()
    print("✅ Script PRO encendido...")
    await client.run_until_disconnected()

asyncio.run(main())