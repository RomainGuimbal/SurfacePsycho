
echo off
Title Update SurfacePsycho asset file

set "current_dir=%CD%"

C:
cd C:\Users\romai\Downloads

for /f %%i in ('dir blender-?.?.?-*.zip /b /a:a /od /t:c') do (
  set LAST_blender_zip=%%i
)

set blender_exe=C:\Users\romai\Downloads\TheBlenders\%LAST_blender_zip:~0,-3%\blender.exe

echo selected Blender :
echo %blender_exe%

cd %current_dir%

%blender_exe% --python %1