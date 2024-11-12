import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import ConversationHandler

# Definimos los estados de la conversación
COURSE, MODULE, EXERCISE, ANSWER, CODE, END = range(6)

# Diccionario para almacenar el estado del curso de cada usuario
user_courses = {}

# Estructura de los módulos para cada lenguaje
modules = {
    'python': [
        {"module": "Introducción", "description": "Aprende lo básico de Python, como variables y operaciones.", "example": "a = 5\nb = 10\nprint(a + b)"},
        {"module": "Condicionales", "description": "Aprende a usar condicionales con if, elif, else.", "example": "x = 10\nif x > 5:\n    print('Mayor que 5')"},
    ],
    'javascript': [
        {"module": "Introducción", "description": "Aprende lo básico de JavaScript, como variables y funciones.", "example": "let a = 5;\nlet b = 10;\nconsole.log(a + b);"},
        {"module": "Funciones", "description": "Aprende a declarar y utilizar funciones.", "example": "function sum(a, b) {\n    return a + b;\n}\nconsole.log(sum(5, 10));"},
    ],
    'sqlite': [
        {"module": "Creación de Tablas", "description": "Aprende a crear tablas en SQLite.", "example": "CREATE TABLE usuarios (id INTEGER PRIMARY KEY, nombre TEXT);"},
        {"module": "Insertar Datos", "description": "Aprende a insertar datos en las tablas.", "example": "INSERT INTO usuarios (nombre) VALUES ('Juan');"},
    ]
}

# Función para comenzar el bot y ofrecer opciones de aprendizaje
async def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_courses[user_id] = {'course': None, 'level': 1, 'module': None}
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
        await update.message.reply_text("Has elegido aprender Python. Elige un módulo:")
        return await choose_module(update, context)

    elif course == '/javascript':
        user_courses[user_id]['course'] = 'javascript'
        await update.message.reply_text("Has elegido aprender JavaScript. Elige un módulo:")
        return await choose_module(update, context)

    elif course == '/sqlite':
        user_courses[user_id]['course'] = 'sqlite'
        await update.message.reply_text("Has elegido aprender SQLite. Elige un módulo:")
        return await choose_module(update, context)

    else:
        await update.message.reply_text("Por favor, elige un curso válido: /python, /javascript o /sqlite.")
        return COURSE

# Función para elegir el módulo
async def choose_module(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    course = user_courses[user_id]['course']

    # Mostrar los módulos disponibles
    available_modules = modules[course]
    module_list = "\n".join([f"{index + 1}. {module['module']}" for index, module in enumerate(available_modules)])
    await update.message.reply_text(f"Elige un módulo:\n{module_list}")
    return MODULE

# Función para mostrar teoría, ejemplos y ejercicio
async def show_module(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    course = user_courses[user_id]['course']
    module_index = int(update.message.text.strip()) - 1

    if module_index < 0 or module_index >= len(modules[course]):
        await update.message.reply_text("Por favor, selecciona un módulo válido.")
        return MODULE

    # Guardamos el módulo seleccionado
    user_courses[user_id]['module'] = module_index
    module = modules[course][module_index]

    # Enviar descripción y ejemplo
    await update.message.reply_text(f"**Módulo: {module['module']}**\n\n{module['description']}\n\nEjemplo de código:\n```\n{module['example']}\n```")
    await update.message.reply_text("Ahora, intenta resolver el ejercicio. Escribe el código que creas que resuelve el problema.")
    return EXERCISE

# Función para manejar la ejecución de código enviado por el usuario
async def execute_code(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    course = user_courses[user_id]['course']
    user_code = update.message.text.strip()
    module_index = user_courses[user_id]['module']
    module = modules[course][module_index]

    if course == 'python':
        try:
            exec(user_code)  # Esta es una operación peligrosa, se debería implementar un entorno seguro
            result = "Código ejecutado con éxito."
        except Exception as e:
            result = f"Hubo un error en el código: {str(e)}"
    elif course == 'javascript':
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
        return await choose_module(update, context)
    else:
        await update.message.reply_text("¡Has completado el curso con éxito! Si deseas empezar de nuevo, usa el comando /start.")
        return END

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
            MODULE: [MessageHandler(filters.TEXT, show_module)],
            EXERCISE: [MessageHandler(filters.TEXT, execute_code)],
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
