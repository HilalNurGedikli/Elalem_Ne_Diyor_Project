@echo off
echo ====================================
echo Python Cache Dosyalarini Temizleme
echo ====================================

echo.
echo 1. __pycache__ klasorlerini temizleniyor...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo 2. .pyc dosyalarini temizleniyor...
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"

echo.
echo 3. .pyo dosyalarini temizleniyor...
for /r . %%f in (*.pyo) do @if exist "%%f" del /q "%%f"

echo.
echo 4. .DS_Store dosyalarini temizleniyor (Mac dosyalari)...
for /r . %%f in (.DS_Store) do @if exist "%%f" del /q "%%f"

echo.
echo 5. Thumbs.db dosyalarini temizleniyor (Windows thumbnail cache)...
for /r . %%f in (Thumbs.db) do @if exist "%%f" del /q "%%f"

echo.
echo ✅ Temizlik tamamlandi!
echo.

echo ====================================
echo Extension Kurulumuna Devam Ediliyor
echo ====================================

echo.
echo 1. Python FastAPI Sunucusunu Baslatiliyor...
cd /d "%~dp0"

echo.
echo Python sanal ortami kontrol ediliyor...
if exist "venv2\Scripts\python.exe" (
    echo ✅ venv2 sanal ortami bulundu
    start "Elalem API Server" cmd /k "venv2\Scripts\activate && python api_server.py"
) else (
    echo ❌ venv2 bulunamadi, sistem Python kullaniliyor
    start "Elalem API Server" cmd /k "python api_server.py"
)

echo.
echo 2. Chrome Extension'i yüklemek için:
echo    - Chrome'da chrome://extensions/ sayfasini açin
echo    - Developer mode'u açin (sag ust kosede)
echo    - "Load unpacked" butonuna tiklayin
echo    - chrome-extension klasörünü seçin
echo.
echo 💡 NOT: Eger "Manifest errors" görürseniz:
echo    - chrome-extension klasörünün içindeki tum dosyalarin oldugunu kontrol edin
echo    - manifest.json dosyasinin syntax hatasi olmadigini kontrol edin

echo.
echo 3. Test etmek için:
echo    - www.sikayetvar.com/trendyol gibi bir sayfaya gidin
echo    - Extension ikonuna tiklayin (sag ust kosede)
echo    - "Bu Siteyi Analiz Et" butonuna tiklayin

echo.
echo 📊 API Server: http://127.0.0.1:8000
echo 📈 API Docs: http://127.0.0.1:8000/docs
echo 🚀 Dashboard: Extension yuklenince otomatik açilacak
echo.

pause
