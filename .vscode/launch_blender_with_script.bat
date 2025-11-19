
echo off
Title Update SurfacePsycho asset file

@REM set "current_dir=%CD%"

@REM @REM Find latest blender.exe
@REM C:
@REM cd C:\Users\romai\Downloads
@REM for /f %%i in ('dir blender-?.?.?-*.zip /b /a:a /od /t:c') do (
@REM   set LAST_blender_zip=%%i
@REM )
@REM set blender_exe=C:\Users\romai\Downloads\TheBlenders\%LAST_blender_zip:~0,-3%\blender.exe
@REM echo Selected Blender : %blender_exe%

@REM cd %current_dir%

set blender_exe=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe

"%blender_exe%" %*