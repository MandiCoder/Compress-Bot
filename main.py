from modules.global_variables import bot, datos_usuarios, progreso_usuarios, detener_progreso
from modules.progress import progress
from modules.utils import show_data
from os.path import basename, join
from os import unlink as borrar
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED
from time import time
from pyrogram import filters, Client
from pyrogram.types import (Message, 
                            CallbackQuery,
                            ReplyKeyboardMarkup, 
                            KeyboardButton,
                            InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            ForceReply)



@bot.app.on_message(filters.command("start"))
def command_start(app: Client, msg: Message):
    msg.reply("Hola")
    datos_usuarios[msg.from_user.username] = []
    
    
    
@bot.app.on_message(filters.regex("rm_"))
def borrar_elemento(app: Client, msg: Message):
    username = msg.from_user.username
    index = msg.text.split("_")[-1]
    datos_usuarios[username].pop(int(index))
    show_data(msg, username)    
    
    
    
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
    


@bot.app.on_message(filters.regex("📋 VER ARCHIVOS") | filters.command("ver_archivos"))
def list_media(app:Client, msg:Message):
    msg.delete()
    show_data(msg, msg.from_user.username)



@bot.app.on_message(filters.reply)
def comprimir_archivos(app:Client, msg:Message):
    msg.reply_to_message.delete()
    
    if msg.reply_to_message.text == "🏷 Introduzca el nombre para el archivo:":
        username:str = msg.from_user.username
        lista_descargas:list = datos_usuarios[username]
        total_archivos:int = len(lista_descargas)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 VER PROGRESO", callback_data="progress")],
            [InlineKeyboardButton("❌ CANCELAR", callback_data="cancel_progreso")]])

        sms:Message = msg.reply_text(f"**🚛 Descargando archivos...\nRestantes: {total_archivos}**",
        reply_markup=markup)

        my_zip = ZipFile(f"{msg.text}.zip", 'w', ZIP_DEFLATED)
        folder = msg.text
        
        for file in lista_descargas:
            start = time()
            archivo = app.download_media(
                message=file,
                file_name=folder + "/",
                progress=progress,
                progress_args=(username, app, start, total_archivos)
            )
            
            if archivo is not None:
                path = join(folder, basename(archivo))
                my_zip.write(path)
                borrar(path)
                total_archivos -= 1
                sms.edit_text(f"**🚛 Descargando archivos...\nRestantes: {total_archivos}**", reply_markup=markup)
            else:
                rmtree(folder)
            
        if archivo is not None:
            my_zip.close()
            datos_usuarios[username].clear()
            sms.edit_text("✅ Finalizado")
            sms.edit_text("**🚚 Enviando a Telegram**")
            app.send_document(msg.chat.id, f"{folder}.zip")
            borrar(f"{folder}.zip")
            sms.delete()
        else:
            my_zip.close()
            borrar(f"{folder}.zip")


@bot.app.on_callback_query()
def enviar_mensaje(app:Client, callback:CallbackQuery):
    msg:Message = callback.message
    username:str = callback.from_user.username
    
    if callback.data == "compress":
        msg.reply_text("**🏷 Introduzca el nombre para el archivo:**", 
                    reply_markup=ForceReply(placeholder="Nombre:"))
        msg.delete()
        
    elif callback.data == "cancel":
        datos_usuarios[username].clear()
        msg.delete()

    
    elif callback.data == "progress":
        callback.answer(progreso_usuarios[username], show_alert=True)


    elif callback.data == "cancel_progreso":
        msg.delete()
        detener_progreso[username] = True
        show_data(msg, username)  
        

if __name__ == '__main__':
    bot.iniciar_bot()