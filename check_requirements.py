#!/usr/bin/env python3
"""
Chrome Extension için gerekli bağımlılıkları kontrol et ve kur
"""
import subprocess
import sys
import os
from pathlib import Path

def check_python_packages():
    """Gerekli Python paketlerini kontrol et"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'selenium',
        'webdriver-manager',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} kurulu")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} eksik")
    
    if missing_packages:
        print(f"\n📦 Eksik paketler kuruluyor: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
    else:
        print("\n✅ Tüm gerekli paketler kurulu!")

def check_chromedriver():
    """ChromeDriver durumunu kontrol et"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # ChromeDriverManager ile test et
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver hazır: {driver_path}")
        return True
    except Exception as e:
        print(f"❌ ChromeDriver hatası: {e}")
        return False

def setup_native_messaging():
    """Native messaging host kurulumu (opsiyonel)"""
    print("\n🔧 Native Messaging Host kurulumu...")
    
    # Registry key oluştur (Windows için)
    if os.name == 'nt':
        try:
            import winreg
            
            # Registry key path
            key_path = r"SOFTWARE\Google\Chrome\NativeMessagingHosts\com.elalem.analyzer"
            
            # Host JSON dosyasının tam yolu
            host_json_path = Path(__file__).parent / "chrome-extension" / "native-messaging-host.json"
            
            # Registry'ye ekle
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, str(host_json_path))
            
            print("✅ Native messaging host kuruldu")
            
        except Exception as e:
            print(f"⚠️ Native messaging kurulumu başarısız: {e}")
            print("   (Bu özellik olmadan da çalışır)")

def main():
    print("🚀 Elalem Chrome Extension Kurulum Kontrolü")
    print("=" * 50)
    
    # Python paketlerini kontrol et
    check_python_packages()
    
    # ChromeDriver'ı kontrol et
    check_chromedriver()
    
    # Native messaging kurulumu (opsiyonel)
    setup_native_messaging()
    
    print("\n" + "=" * 50)
    print("🎉 Kurulum kontrolü tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. setup_extension.bat dosyasını çalıştırın")
    print("2. Chrome'da chrome://extensions/ sayfasını açın")
    print("3. Developer mode'u açın")
    print("4. 'Load unpacked' ile chrome-extension klasörünü yükleyin")
    print("5. Desteklenen bir siteye gidin ve test edin")

if __name__ == "__main__":
    main()
