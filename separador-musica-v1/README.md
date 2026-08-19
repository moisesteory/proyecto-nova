# Separador de Música V1

Aplicación Windows para separar una canción en **Voz.wav** e **Instrumental.wav** usando Demucs.

## Ejecutar desde código

Abre PowerShell en esta carpeta y ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build-windows.ps1
```

El ejecutable queda en `dist\SeparadorMusica.exe`.

## Uso

1. Abre `SeparadorMusica.exe`.
2. Selecciona una canción.
3. Elige la carpeta de salida.
4. Pulsa **Separar voz e instrumental**.
5. Dentro de una carpeta con el nombre de la canción aparecerán `Voz.wav` e `Instrumental.wav`.

La primera separación necesita descargar el modelo de IA y puede tardar más. Las siguientes reutilizan la caché del modelo.
