# Cómo generar el instalable (.exe) de SGV

Estos pasos se ejecutan en una computadora con **Windows** (no funciona desde Mac/Linux para generar .exe).

## Requisitos previos
- Tener Python instalado (3.10 o superior).
- Tener este proyecto descomprimido en una carpeta.

## Pasos

1. Abre una terminal (CMD o PowerShell) dentro de la carpeta `sgv 4` (donde está `main.py`).

2. Ejecuta el script automático que ya viene incluido:
   ```
   build_exe.bat
   ```
   Esto va a:
   - Instalar las dependencias del `requirements.txt`
   - Instalar `flet`
   - Generar el ejecutable con `flet pack`

3. Cuando termine, vas a encontrar el ejecutable en:
   ```
   dist\SGV.exe
   ```

## Cómo entregar/usar el programa

- Copia el archivo `dist\SGV.exe` a la carpeta donde quieras que viva el programa (puede ser una carpeta nueva, USB, etc.).
- La primera vez que lo abras, se creará automáticamente el archivo `sgv.db` (la base de datos) **en la misma carpeta** donde esté el `.exe`. Ese archivo es el que guarda todos los productos, ventas, usuarios, etc.
- Para entregar el programa a otra persona, copia **`SGV.exe`** junto con el `sgv.db` (si quieres que lleve los datos ya cargados), o solo `SGV.exe` si quieres que arranque con la base de datos limpia (con los datos de ejemplo iniciales).
- No es necesario tener Python instalado en la computadora donde se vaya a usar el `.exe`.

## Notas
- El primer arranque del `.exe` puede tardar unos segundos más de lo normal (es normal en aplicaciones empaquetadas con PyInstaller).
- Si Windows muestra una advertencia de "Windows protegió tu PC" (SmartScreen), haz clic en "Más información" → "Ejecutar de todas formas". Esto pasa porque el ejecutable no tiene una firma digital (normal para proyectos académicos).
