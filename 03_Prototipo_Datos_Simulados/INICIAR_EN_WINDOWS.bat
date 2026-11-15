@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ================================================
echo RED METROPOLITANA - DEMO CON DATOS SIMULADOS
 echo ================================================
where py >nul 2>nul
if %errorlevel%==0 (
  py -m pip install -r requirements.txt
  if errorlevel 1 goto error
  py ejecutar_demo.py
  if errorlevel 1 goto error
  py -m unittest discover -s tests -v
) else (
  where python >nul 2>nul
  if errorlevel 1 goto missing
  python -m pip install -r requirements.txt
  if errorlevel 1 goto error
  python ejecutar_demo.py
  if errorlevel 1 goto error
  python -m unittest discover -s tests -v
)
if errorlevel 1 goto error
start "" "resultado\Dashboard_DEMO_Abrir.html"
echo Todo listo. Recuerda: 100%% datos SIMULADOS.
pause
exit /b 0
:missing
echo No se encontro Python. Instalalo desde https://www.python.org/downloads/
pause
exit /b 2
:error
echo Ha ocurrido un error. Revisa requirements y ejecucion.
pause
exit /b 1
