import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Función para comenzar el bot y ofrecer opciones de aprendizaje
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "¡Hola! Bienvenido al bot de aprendizaje de programación. "
        "Elige una opción para aprender:\n"
        "/python - Aprender Python\n"
        "/javascript - Aprender JavaScript\n"
        "/sqlite - Aprender SQLite"
    )

# Funciones específicas de aprendizaje
async def python_course(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Empezamos con Python! Aquí tienes algunos conceptos básicos y ejercicios...")

async def javascript_course(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("¡Aprendamos JavaScript! Aquí tienes algunos conceptos y ejercicios básicos...")

async def sqlite_course(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Comenzamos con SQLite. Vamos a ver algunos ejemplos prácticos de bases de datos...")

# Configuración del bot
def main():
    token = os.getenv("TELEGRAM_TOKEN")  # Asegúrate de tener el token en una variable de entorno
    application = Application.builder().token(token).build()

    # Agregar manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("python", python_course))
    application.add_handler(CommandHandler("javascript", javascript_course))
    application.add_handler(CommandHandler("sqlite", sqlite_course))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
