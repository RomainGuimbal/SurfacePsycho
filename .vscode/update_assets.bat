
echo off
Title Update SurfacePsycho asset file

set "current_dir=%CD%"

@REM Find latest blender.exe
C:
cd C:\Users\romai\Downloads

for /f %%i in ('dir blender-?.?.?-*.zip /b /a:a /od /t:c') do (
  set LAST_blender_zip=%%i
)
set blender_exe=C:\Users\romai\Downloads\TheBlenders\%LAST_blender_zip:~0,-3%\blender.exe
echo selected Blender : %blender_exe%

cd %current_dir%

%blender_exe% --background "C:\Users\romai\Documents\Projets\26 - Bezier Quest\SurfacePsycho\assets\assets.blend" ^
--python "Asset Importer.py"