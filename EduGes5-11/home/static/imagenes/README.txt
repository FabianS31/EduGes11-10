Notas sobre estáticos duplicados

He copiado `styles.css` a `home/static/usuarios/`.

Limitación: las imágenes (PNG/JPG) no pueden ser leídas ni copiadas por esta herramienta porque son archivos binarios. Los archivos originales siguen en:

  usuarios/static/usuarios/

Si querés duplicar las imágenes a `home/static/usuarios/` en tu máquina Windows (PowerShell), ejecuta en una terminal (desde la raíz del proyecto):

  # copia recursiva de solo imágenes PNG/JPG
  Copy-Item -Path .\usuarios\static\usuarios\*.png -Destination .\home\static\usuarios\ -Force
  Copy-Item -Path .\usuarios\static\usuarios\*.jpg -Destination .\home\static\usuarios\ -Force

O para copiar todo el contenido estático tal cual:

  Copy-Item -Path .\usuarios\static\usuarios\* -Destination .\home\static\usuarios\ -Recurse -Force

Después de copiar las imágenes podés correr `python manage.py collectstatic` si usás ese flujo, o simplemente recargar la página en modo DEBUG (las apps ya exponen sus staticdirs en dev).

Si querés, puedo intentar ejecutar esos comandos aquí (necesito permiso) o dejás que los ejecutes localmente.