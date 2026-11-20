# GitHub Codespaces ♥️ Flask

Welcome to your shiny new Codespace running Flask! We've got everything fired up and running for you to explore Flask.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with the what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

To run this application:

```
flask --debug run
```

## Desplegar en Render

1. Crea un repositorio en GitHub y publica esta rama:

   ```bash
   git add .
   git commit -m "Preparar despliegue en Render"
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

2. En Render, selecciona **New > Blueprint** y conecta el repositorio.
3. Render detectara `render.yaml` y configurara el servicio `kaffe`.
4. Como alternativa manual, usa:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Health Check Path: `/estado`

La base de datos SQLite incluida es temporal en Render: los datos se reinician al
volver a desplegar o reiniciar el servicio. Para usuarios y pedidos persistentes,
configura una base PostgreSQL administrada de Render.
