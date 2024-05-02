from .global_variables import datos_usuarios
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sizeof(num: int, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)





def show_data(msg):
    username = msg.from_user.username
    if username not in datos_usuarios:
        datos_usuarios[username] = []
    
    texto:str = "**💠 Archivos para comprimir: **\n"
    total_size:int = 0
    
    for i in datos_usuarios[username]:
        media_value = i.media.value
        
        if media_value == 'document':
            total_size += i.document.file_size
            texto += f"**\n📄 `{sizeof(i.document.file_size)}` - {i.document.file_name}**"

        if media_value == 'photo':
            total_size += i.photo.file_size
            texto += f"**\n📷 `{sizeof(i.photo.file_size)}` - Ancho: `{i.photo.width}` / Alto: `{i.photo.height}`**"

        if media_value == 'sticker':
            total_size += i.sticker.file_size
            texto += f"**\n🧩 `{sizeof(i.sticker.file_size)}` - Sticker [{i.sticker.emoji}]**"
        
        if media_value == 'audio':
            total_size += i.audio.file_size
            texto += f"**\n🎧 `{sizeof(i.audio.file_size)}` - {i.audio.file_name}**"
        
        if media_value == 'video':
            total_size += i.video.file_size
            texto += f"**\n🎬 `{sizeof(i.video.file_size)}` - {i.video.file_name}**"
        
        
    texto += f"\n\n**📌 Tamaño total: {sizeof(total_size)}**"
    msg.reply(texto, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 COMPRIMIR", callback_data="compress")]
    ]))
