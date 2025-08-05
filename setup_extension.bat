@echo off
echo =================================
echo Elalem Chrome Extension Kurulumu
echo =================================

echo.
echo 1. Python FastAPI Sunucusunu Baslatiliyor...
cd /d "%~dp0"
start "Elalem API Server" cmd /k "venv2\Scripts\activate && python api_server.py"

echo.
echo 2. Chrome Extension'i yüklemek için:
echo    - Chrome'da chrome://extensions/ sayfasini açin
echo    - Developer mode'u açin
echo    - "Load unpacked" butonuna tiklayin
echo    - chrome-extension klasörünü seçin

echo.
echo 3. Test etmek için:
echo    - www.sikayetvar.com/trendyol gibi bir sayfaya gidin
echo    - Extension ikonuna tiklayin
echo    - "Bu Siteyi Analiz Et" butonuna tiklayin

echo.
echo API Server: http://127.0.0.1:8000
echo Dashboard: API çalişinca otomatik açilacak
echo.

pause
