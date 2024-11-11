import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import ConversationHandler

# Definimos los estados de la conversación
COURSE, EXERCISE, ANSWER, CODE, END = range(5)

# Diccionario para almacenar el estado del curso de cada usuario
user_courses = {}

# Función para comenzar el bot y ofrecer opciones de aprendizaje
async def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_courses[user_id] = {'course': None, 'level': 1}
    await update.message.reply_text(
        "¡Hola! Bienvenido al bot de aprendizaje de programación. "
        "Elige una opción para aprender:\n"
        "/python - Aprender Python\n"
        "/javascript - Aprender JavaScript\n"
        "/sqlite - Aprender SQLite"
    )
    return COURSE

# Función para seleccionar el curso
async def choose_course(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    course = update.message.text.lower().strip()

    if course == '/python':
        user_courses[user_id]['course'] = 'python'
        await update.message.reply_text("Has elegido aprender Python. Comencemos con un ejercicio.")
        return await python_exercise(update, context)

    elif course == '/javascript':
        user_courses[user_id]['course'] = 'javascript'
        await update.message.reply_text("Has elegido aprender JavaScript. Comencemos con un ejercicio.")
        return await javascript_exercise(update, context)

    elif course == '/sqlite':
        user_courses[user_id]['course'] = 'sqlite'
        await update.message.reply_text("Has elegido aprender SQLite. Comencemos con un ejercicio.")
        return await sqlite_exercise(update, context)

    else:
        await update.message.reply_text("Por favor, elige un curso válido: /python, /javascript o /sqlite.")
        return COURSE

# Ejercicio de Python
async def python_exercise(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    level = user_courses[user_id]['level']

    if level == 1:
        await update.message.reply_text("Escribe un código en Python para imprimir 'Hola, mundo'.")
        return CODE
    elif level == 2:
        await update.message.reply_text("Escribe un código en Python para sumar dos números.")
        return CODE
    else:
        await update.message.reply_text("¡Felicidades! Has completado el curso de Python.")
        return END

# Ejercicio de JavaScript
async def javascript_exercise(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    level = user_courses[user_id]['level']

    if level == 1:
        await update.message.reply_text("Escribe un código en JavaScript para imprimir 'Hola, mundo'.")
        return CODE
    elif level == 2:
        await update.message.reply_text("Escribe un código en JavaScript para sumar dos números.")
        return CODE
    else:
        await update.message.reply_text("¡Felicidades! Has completado el curso de JavaScript.")
        return END

# Ejercicio de SQLite
async def sqlite_exercise(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    level = user_courses[user_id]['level']

    if level == 1:
        await update.message.reply_text("Escribe una consulta en SQLite para crear una tabla llamada 'usuarios'.")
        return CODE
    elif level == 2:
        await update.message.reply_text("Escribe una consulta en SQLite para insertar un registro en la tabla 'usuarios'.")
        return CODE
    else:
        await update.message.reply_text("¡Felicidades! Has completado el curso de SQLite.")
        return END

# Función para manejar la ejecución de código enviado por el usuario
async def execute_code(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    course = user_courses[user_id]['course']
    user_code = update.message.text.strip()

    if course == 'python':
        # Ejecutar código Python de manera controlada
        try:
            exec(user_code)  # Esta es una operación peligrosa, se debería implementar un entorno seguro
            result = "Código ejecutado con éxito."
        except Exception as e:
            result = f"Hubo un error en el código: {str(e)}"
    elif course == 'javascript':
        # Ejecutar código JavaScript usando node.js
        try:
            process = subprocess.Popen(
                ['node', '-e', user_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            if stderr:
                result = f"Error en el código: {stderr.decode()}"
            else:
                result = f"Resultado: {stdout.decode()}"
        except Exception as e:
            result = f"Hubo un error al ejecutar el código: {str(e)}"
    elif course == 'sqlite':
        # Ejecutar consulta SQLite en una base de datos en memoria
        import sqlite3
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            cursor.execute(user_code)
            result = "Consulta ejecutada con éxito."
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            result = f"Hubo un error con la consulta SQL: {e}"

    # Mostrar el resultado al usuario
    await update.message.reply_text(result)

    # Avanzar a la siguiente pregunta o terminar el curso
    user_courses[user_id]['level'] += 1
    if user_courses[user_id]['level'] <= 2:
        return await choose_course(update, context)
    else:
        return END

# Función para finalizar el curso
async def end(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("¡Has completado el curso con éxito! Si deseas empezar de nuevo, usa el comando /start.")
    return ConversationHandler.END

# Configuración del bot
def main():
    token = os.getenv("TELEGRAM_TOKEN")  # Asegúrate de tener el token en una variable de entorno

    # Crear la aplicación de Telegram y el manejador de comandos
    application = Application.builder().token(token).build()

    # Manejo de conversación
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            COURSE: [MessageHandler(filters.TEXT, choose_course)],
            CODE: [MessageHandler(filters.TEXT, execute_code)],
            END: [MessageHandler(filters.TEXT, end)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Agregar el manejador de conversación
    application.add_handler(conversation_handler)

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
