
@echo off
setlocal

echo ==========================================
echo       YT Downloader - Windows Build
echo ==========================================
echo.

cd /d "%~dp0"

set "DENO_SOURCE=%USERPROFILE%\.deno\bin\deno.exe"
set "FFMPEG_SOURCE=C:\ffmpeg-2024-11-18-git-970d57988d-essentials_build\bin"

echo Checking runtime files...

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Project virtual environment not found.
    goto failed
)

if not exist "%DENO_SOURCE%" (
    echo ERROR: Deno executable not found.
    goto failed
)

if not exist "%FFMPEG_SOURCE%\ffmpeg.exe" (
    echo ERROR: FFmpeg executable not found.
    goto failed
)

if not exist "%FFMPEG_SOURCE%\ffprobe.exe" (
    echo ERROR: FFprobe executable not found.
    goto failed
)

echo.
echo Building Python application with PyInstaller...
echo.

".venv\Scripts\python.exe" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onedir ^
    --console ^
    --name "YT Downloader" ^
    --collect-all yt_dlp ^
    --collect-all yt_dlp_ejs ^
    main.py

if errorlevel 1 goto failed

echo.
echo Copying bundled runtime files...

mkdir "dist\YT Downloader\runtime\ffmpeg"

copy /Y "%DENO_SOURCE%" "dist\YT Downloader\runtime\deno.exe" >nul
if errorlevel 1 goto failed

copy /Y "%FFMPEG_SOURCE%\ffmpeg.exe" "dist\YT Downloader\runtime\ffmpeg\ffmpeg.exe" >nul
if errorlevel 1 goto failed

copy /Y "%FFMPEG_SOURCE%\ffprobe.exe" "dist\YT Downloader\runtime\ffmpeg\ffprobe.exe" >nul
if errorlevel 1 goto failed

copy /Y "LICENSE" "dist\YT Downloader\LICENSE" >nul
if errorlevel 1 goto failed

copy /Y "THIRD_PARTY_NOTICES.md" "dist\YT Downloader\THIRD_PARTY_NOTICES.md" >nul
if errorlevel 1 goto failed

echo.
echo Copying third-party licence files...

mkdir "dist\YT Downloader\licenses" 2>nul

copy /Y "licenses\BROTLI-LICENSE.txt" "dist\YT Downloader\licenses\BROTLI-LICENSE.txt" >nul
if errorlevel 1 goto failed

copy /Y "licenses\CERTIFI-LICENSE.txt" "dist\YT Downloader\licenses\CERTIFI-LICENSE.txt" >nul
if errorlevel 1 goto failed

copy /Y "licenses\CHARSET-NORMALIZER-LICENSE.txt" "dist\YT Downloader\licenses\CHARSET-NORMALIZER-LICENSE.txt" >nul
if errorlevel 1 goto failed

copy /Y "licenses\PYCRYPTODOMEX-LICENSE.txt" "dist\YT Downloader\licenses\PYCRYPTODOMEX-LICENSE.txt" >nul
if errorlevel 1 goto failed

echo.
echo ==========================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo Application location:
echo dist\YT Downloader\
echo.
pause
exit /b 0

:failed
echo.
echo ==========================================
echo BUILD FAILED!
echo ==========================================
echo Check the error messages above.
echo.
pause
exit /b 1
