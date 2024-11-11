import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Función para comenzar el bot y ofrecer opciones de aprendizaje
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "¡Hola! Bienvenido al bot de aprendizaje de programación. "
        "Elige una opción para aprender:\n"
        "/python - Aprender Python\n"
        "/javascript - Aprender JavaScript\n"
        "/sqlite - Aprender SQLite"
    )

# Funciones específicas de aprendizaje
def python_course(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("¡Empezamos con Python! Aquí tienes algunos conceptos básicos y ejercicios...")

def javascript_course(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("¡Aprendamos JavaScript! Aquí tienes algunos conceptos y ejercicios básicos...")

def sqlite_course(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Comenzamos con SQLite. Vamos a ver algunos ejemplos prácticos de bases de datos...")

# Configuración del bot
def main():
    token = os.getenv("TELEGRAM_TOKEN")  # Asegúrate de tener el token en una variable de entorno
    updater = Updater(token)

    # Agregar manejadores de comandos
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("python", python_course))
    updater.dispatcher.add_handler(CommandHandler("javascript", javascript_course))
    updater.dispatcher.add_handler(CommandHandler("sqlite", sqlite_course))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()