import jinja2
import os
from aiohttp import web
from aiohttp import streamer

"""==============Envio de el Archivo por HTTP================="""

@streamer
async def file_sender(writer, file_path=None):
    with open(file_path, "rb") as f:
        chunk = f.read(2**16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2**16)

"""===============Servicio de Recepcion de la Peticion GET==================="""

async def download_file(request):
    """
    La función `download_file` es una función asíncrona que descarga un archivo especificado por los
    parámetros `file_name` y `route` y lo devuelve como una respuesta web.

    :param request: El parámetro `request` es un objeto que representa la solicitud HTTP realizada por
    el cliente. Contiene información como el método de solicitud, encabezados, parámetros de URL y el
    cuerpo de la solicitud. En este fragmento de código, se utiliza para extraer `file_name` y `route`
    de la ruta URL
    :return: un objeto web.Response.
    """
    file_name = request.match_info["file_name"]
    route = request.match_info["route"]

    file_path = os.path.join('downloads', route, file_name)
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(
            file_name=file_name
        ),
        "Accept-Ranges": "bytes",
        "Content-Type": f'{file_path.split("/")[-1].split(".")[-1]}',
        "Content-Length": str(os.path.getsize(file_path)),
    }

    if not os.path.exists(file_path):
        return web.Response(
            body="El Archivo  <{file_name}> No Existe".format(file_name=file_name),
            status=404,
        )

    return web.Response(body=file_sender(file_path=file_path), headers=headers)



async def index(request):
    file_path = "./templates/index.html"
    # Envio de Parametros al HTML
    nombre = "Rey"
    data = {"nombre": nombre, "estilos": "styles.css"}
    with open(file_path, "r") as file:
        template = jinja2.Template(file.read())
        html = template.render(data)
    return web.Response(text=html, content_type="text/html")