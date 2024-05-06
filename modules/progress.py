from .global_variables import detener_progreso, progreso_usuarios
import time


def update_progress_bar(inte, max):
    percentage = inte / max
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 10 - hashes
    progress_bar = "[" + "■" * hashes + "□" * spaces + "]"
    percentage_pos = int(hashes / 1)
    percentage_string = "[" + str(percentage) + "%" + "]"
    progress_bar = (
        progress_bar[:percentage_pos]
        + percentage_string
        + progress_bar[percentage_pos + len(percentage_string) :]
    )
    return progress_bar


def progress(current, total, username, app, inicio_tiempo, rest):
    if username not in detener_progreso:
        detener_progreso[username] = False

    if detener_progreso[username]:
        app.stop_transmission()

    tiempo_transcurrido = time.time() - inicio_tiempo
    velocidad = tiempo_transcurrido / current if current > 0 else 0  # Evitar división por cero
    tiempo_restante = (total - current) * velocidad
    speed = round((round(current / 1000000, 2) / tiempo_transcurrido), 2)

    horas_restantes = int(tiempo_restante // 3600)
    minutos_restantes = int((tiempo_restante % 3600) // 60)
    segundos_restantes = int(tiempo_restante % 60)

    txt = f"🚛 Descargando...\n{update_progress_bar(current, total)}"
    txt += f"\n\n📁 Archivos pendientes: {rest}"
    txt += f"\n📊 Total :{round(total/1000000,2)} MB"
    txt += f"\n📲 Descargado: {round(current/1000000,2)} MB"
    txt += f"\n⏰ ETA: {horas_restantes:02d}:{minutos_restantes:02d}:{segundos_restantes:02d}"
    txt += f"\n🚀 Velocidad: {speed} MB/s"

    progreso_usuarios[username] = txt
    