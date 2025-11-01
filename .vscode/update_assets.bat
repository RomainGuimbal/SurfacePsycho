
echo off
Title Update SurfacePsycho asset file

C:
cd C:\Users\romai\Downloads

for /f %%i in ('dir blender-?.?.?-*.zip /b /a:a /od /t:c') do (
  set LAST_blender_zip=%%i
)

set blender_exe=C:\Users\romai\Downloads\TheBlenders\%LAST_blender_zip:~0,-3%\blender.exe

echo selected Blender :
echo %blender_exe%

start %blender_exe% --background "C:\Users\romai\Documents\Projets\26 - Bezier Quest\SurfacePsycho\assets\assets.blend" ^
--python "C:\Users\romai\Documents\Projets\26 - Bezier Quest\SurfacePsycho\assets\Asset Importer.py"