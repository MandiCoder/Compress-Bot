from modules.global_variables import bot, datos_usuarios
from modules.utils import show_data
from os.path import basename, join
from os import unlink as borrar
from zipfile import ZipFile, ZIP_DEFLATED
from pyrogram import filters, Client
from pyrogram.types import (Message, 
                            CallbackQuery,
                            ReplyKeyboardMarkup, 
                            KeyboardButton,
                            ForceReply)



@bot.app.on_message(filters.command("start"))
def command_start(app, msg):
    msg.reply("Hola")
    datos_usuarios[msg.from_user.username] = []
    
    
    
@bot.app.on_message(filters.media)
def get_media(app: Client, msg: Message):
    msg.reply("**🗄 Archivo cargado**", 
              quote=True, 
              reply_markup=ReplyKeyboardMarkup([
                  [KeyboardButton("📋 VER ARCHIVOS")]
              ], resize_keyboard=True, one_time_keyboard=True)
              )
    username = msg.from_user.username
    if username not in datos_usuarios:
        datos_usuarios[username] = []
    datos_usuarios[username].append(msg)
    


@bot.app.on_message(filters.regex("📋 VER ARCHIVOS"))
def list_media(app:Client, msg:Message):
    msg.delete()
    show_data(msg)



@bot.app.on_message(filters.reply)
def comprimir_archivos(app:Client, msg:Message):
    msg.reply_to_message.delete()
    
    if msg.reply_to_message.text == "🏷 Introduzca el nombre para el archivo:":
        username:str = msg.from_user.username
        lista_descargas:list = datos_usuarios[username]
        total_archivos:int = len(lista_descargas)
        sms:Message = msg.reply_text(f"**🚛 Descargando archivos...\nRestantes: {total_archivos}**")
        my_zip = ZipFile(f"{msg.text}.zip", 'w', ZIP_DEFLATED)
        folder = msg.text
        
        for file in lista_descargas:
            archivo = app.download_media(
                message=file,
                file_name=folder + "/"
            )
            path = join(folder, basename(archivo))
            my_zip.write(path)
            borrar(path)
            total_archivos -= 1
            sms.edit_text(f"**🚛 Descargando archivos...\nRestantes: {total_archivos}**")
            
        datos_usuarios[username].clear()
        my_zip.close()
        sms.edit_text("✅ Finalizado")
        sms.edit_text("**🚚 Enviando a Telegram**")
        app.send_document(msg.chat.id, f"{folder}.zip")
        borrar(f"{folder}.zip")
        sms.delete()

@bot.app.on_callback_query()
def enviar_mensaje(app:Client, callback:CallbackQuery):
    msg:Message = callback.message
    msg.delete()
    msg.reply_text("**🏷 Introduzca el nombre para el archivo:**", 
                   reply_markup=ForceReply(placeholder="Nombre:"))
    


if __name__ == '__main__':
    bot.iniciar_bot()