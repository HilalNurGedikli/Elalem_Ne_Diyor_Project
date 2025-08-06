# 🔍 Elalem Ne Diyor Project

> **Gerçek kullanıcı deneyimlerini analiz eden akıllı platform**

Türkiye'deki e-ticaret sitelerini ve markaları analiz eden, şikayetvar, ekşi sözlük, sosyal medya gibi platformlardan veri toplayan ve AI ile değerlendiren kapsamlı analiz sistemi.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Chrome Extension](#-chrome-extension)
- [API Endpoints](#-api-endpoints)
- [Teknolojiler](#-teknolojiler)
- [Proje Yapısı](#-proje-yapısı)
- [Veri Kaynakları](#-veri-kaynakları)
- [Konfigürasyon](#-konfigürasyon)
- [Geliştirme](#-geliştirme)
- [Sorun Giderme](#-sorun-giderme)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## ✨ Özellikler

### 🔍 **Kapsamlı Veri Toplama**
- **Şikayetvar.com**: Müşteri şikayetleri ve çözüm süreçleri
- **Ekşi Sözlük**: Kullanıcı deneyimleri ve genel görüşler  
- **Instagram**: Sosyal medya etkileşimleri ve yorumlar
- **Twitter**: Anlık geri bildirimler ve şikayetler
- **ETBİS**: E-ticaret kayıt durumu kontrolü

### 🤖 **AI Destekli Analiz**
- Google Gemini AI ile akıllı değerlendirme
- Otomatik güvenilirlik skorlaması
- Kullanıcı memnuniyet analizi
- Kronik problem tespiti
- Formatlanmış sonuç raporları

### 🌐 **Chrome Extension**
- Her sitede kullanılabilir analiz butonu
- Gerçek zamanlı veri toplama
- Manuel site arama özelliği
- Popup interface ile kolay erişim
- Headless browser desteği

### 💾 **Cache & Performans**
- Akıllı cache sistemi (30 dakika)
- Otomatik veri temizleme
- Hızlı tekrar erişim
- Background işleme desteği

## 🚀 Kurulum

### Ön Gereksinimler

```bash
# Python 3.8+
python --version

# Node.js (Extension için)
node --version

# Chrome Browser
```

### 1. Proje Kurulumu

```bash
# Repoyu klonla
git clone https://github.com/HilalNurGedikli/Elalem_Ne_Diyor_Project.git
cd Elalem_Ne_Diyor_Project

# Virtual environment oluştur
python -m venv venv2
venv2\Scripts\activate  # Windows
# source venv2/bin/activate  # Linux/Mac

# Gerekli paketleri yükle
pip install -r requirements.txt
```

### 2. Konfigürasyon

#### .env Dosyası Konfigürasyonu

Projeyi çalıştırmadan önce `.env` dosyasını oluşturun ve aşağıdaki environment variable'ları tanımlayın:

```bash
# Google Gemini AI API Anahtarı (Zorunlu)
GEMINI_API_KEY=your_gemini_api_key_here

# Twitter API Konfigürasyonu (İsteğe Bağlı)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here

# ChromeDriver Konfigürasyonu (Selenium için)
CHROMEDRIVER_PATH=./services/chromedriver.exe
CHROMEDRIVER_FALLBACK_PATH=C:\Users\gzmns\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe
```

#### API Anahtarları Nasıl Alınır:

**Gemini API Key:**
1. [Google AI Studio](https://makersuite.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan anahtarı `.env` dosyasındaki `GEMINI_API_KEY` yerine yazın

**Twitter API Keys (Opsiyonel):**
1. [Twitter Developer Portal](https://developer.twitter.com/) adresine gidin
2. Geliştirici hesabı oluşturun veya mevcut hesabınızla giriş yapın
3. Yeni bir App oluşturun
4. API Keys and Tokens bölümünden gerekli anahtarları alın

#### Güvenlik Notları:
- `.env` dosyasını asla version control'e eklemeyin
- API anahtarlarınızı kimseyle paylaşmayın
- Üretim ortamında environment variable'ları sistem düzeyinde tanımlayın

#### Ek Konfigürasyon

`.env` dosyasını oluşturduktan sonra:

```properties
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=True
PORT=8000
```

### 3. ChromeDriver Kurulumu

```bash
# Chrome sürümünüze uygun ChromeDriver indirin
# https://chromedriver.chromium.org/
# veya WebDriverManager otomatik indirecektir
```

## 🎯 Kullanım

### Server Başlatma

```bash
# Ana server (FastAPI)
python main.py

# Sadece analiz router'ı
uvicorn routers.analyze:router --reload --port 8001

# Extension test server'ı
cd chrome-extension
python -m http.server 8080
```

### Temel API Kullanımı

```bash
# Site analizi
curl "http://127.0.0.1:8000/analyze?site=trendyol"

# Formatlanmış analiz
curl "http://127.0.0.1:8001/analyze-formatted?site=amazon"

# Server durumu
curl "http://127.0.0.1:8001/status"
```

## 🧩 Chrome Extension

### Kurulum

1. Chrome'da `chrome://extensions/` açın
2. "Geliştirici modu"nu etkinleştirin
3. "Paketlenmemiş uzantı yükle" ile `chrome-extension` klasörünü seçin

### Kullanım

1. **Otomatik Analiz**: Herhangi bir sitede sağ üstteki "🔍 Elalem Analizi" butonuna tıklayın
2. **Manuel Arama**: Extension popup'ından site adı girerek arama yapın
3. **Sonuçları Görüntüleme**: Analiz sonuçları sayfada popup olarak görünür

### Extension Özellikleri

- ✅ Tüm siteler desteklenir
- ✅ E-ticaret platformu otomatik tespiti
- ✅ Arama terimi desteği
- ✅ Popup interface
- ✅ Real-time API iletişimi

## 📡 API Endpoints

### Analiz Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `GET` | `/analyze?site={site}` | Temel site analizi |
| `GET` | `/analyze-formatted?site={site}` | Formatlanmış analiz |
| `POST` | `/analyze` | Detaylı analiz (JSON body) |
| `GET` | `/status` | Server durumu |

### Örnek Yanıt

```json
{
  "site": "trendyol",
  "success": true,
  "analysis": {
    "sections": [
      {
        "title": "🛡️ Güvenilirlik",
        "content": "ETBİS kayıtlı, güvenilir platform",
        "icon": "🛡️",
        "type": "security"
      }
    ]
  },
  "yorum_sayısı": 25,
  "rating": "7/10"
}
```

## 🛠 Teknolojiler

### Backend
- **FastAPI**: Modern Python web framework
- **Selenium**: Web scraping ve otomasyon
- **BeautifulSoup**: HTML parsing
- **Google Gemini AI**: Doğal dil işleme
- **Requests**: HTTP istekleri
- **JSON**: Veri depolama

### Frontend
- **Vanilla JavaScript**: Extension mantığı
- **Chrome Extension API**: Browser entegrasyonu
- **HTML/CSS**: Kullanıcı arayüzü
- **Fetch API**: HTTP istekleri

### DevOps
- **Uvicorn**: ASGI server
- **WebDriverManager**: Otomatik driver yönetimi
- **Python-dotenv**: Environment değişkenleri

## 📁 Proje Yapısı

```
Elalem_Ne_Diyor_Project/
├── 📁 chrome-extension/          # Chrome Extension dosyaları
│   ├── manifest.json             # Extension manifest
│   ├── popup.html                # Popup arayüzü
│   ├── popup.js                  # Popup JavaScript
│   ├── content.js                # İçerik scripti
│   ├── background.js             # Arka plan scripti
│   └── analysis.html             # Analiz sonuçları sayfası
├── 📁 routers/                   # FastAPI router'ları
│   └── analyze.py                # Ana analiz endpoint'leri
├── 📁 services/                  # Servis dosyaları
│   ├── site_lookup.py            # Şikayetvar scraping
│   ├── eksi_api.py               # Ekşi Sözlük API
│   ├── gemini_utils.py           # Gemini AI entegrasyonu
│   ├── insta_api.py              # Instagram veri çekme
│   ├── twitterdan_jsona_cek.py   # Twitter API
│   └── etbis_kayitlimi.py        # ETBİS kontrol
├── 📁 veriler/                   # Veri depolama
│   ├── json/                     # JSON veri dosyaları
│   └── txt/                      # Text veri dosyaları
├── main.py                       # Ana server dosyası
├── yorumlari_json_oku.py         # JSON okuma utilities
├── requirements.txt              # Python bağımlılıkları
├── .env                          # Environment değişkenleri
├── analyze_cache.json            # Analiz cache dosyası
└── README.md                     # Bu dosya
```

## 🗂 Veri Kaynakları

### 1. Şikayetvar.com
- **Kullanım**: Müşteri şikayetleri ve çözüm süreçleri
- **Metod**: Selenium web scraping
- **Format**: JSON object array
- **Özellikler**: Tarih, yorum metni, kategori

### 2. Ekşi Sözlük
- **Kullanım**: Kullanıcı deneyimleri ve görüşler
- **Metod**: ChromeDriver + BeautifulSoup
- **Format**: Entry listesi
- **Özellikler**: Çok sayfalı scraping desteği

### 3. Sosyal Medya
- **Instagram**: Hashtag ve mention analizi
- **Twitter**: Gerçek zamanlı mention tracking
- **Format**: API response JSON

### 4. ETBİS
- **Kullanım**: E-ticaret kayıt durumu
- **Metod**: Resmi site kontrolü
- **Format**: Boolean + detay mesajı

## ⚙️ Konfigürasyon

### Environment Değişkenleri

```properties
# API Keys
GEMINI_API_KEY=your_gemini_api_key
TWITTER_BEARER_TOKEN=your_twitter_token

# Server Settings
DEBUG=True
PORT=8003
HOST=127.0.0.1

# Cache Settings
CACHE_DURATION_MINUTES=30

# Browser Settings
HEADLESS_MODE=True
CHROME_DRIVER_PATH=auto
```

### Cache Ayarları

```python
# analyze.py içinde
CACHE_DURATION_MINUTES = 30  # Cache süresi
CACHE_FILE = "analyze_cache.json"  # Cache dosyası
```

## 👨‍💻 Geliştirme

### Development Server

```bash
# Auto-reload ile development
uvicorn main:app --reload --port 8000

# Extension development server
cd chrome-extension && python -m http.server 8080
```

### Debug Modu

```bash
# Detaylı loglarla çalıştırma
DEBUG=True python main.py

# Sadece belirli servisler
python -c "from services.site_lookup import scrape_sikayetvar; print(scrape_sikayetvar('test'))"
```

### Test Etme

```bash
# API test
curl -X GET "http://127.0.0.1:8000/analyze?site=test"

# Extension test sayfası
open chrome-extension/test-page.html
```

## 🔧 Sorun Giderme

### Yaygın Sorunlar

#### 1. ChromeDriver Uyumsuzluğu
```bash
# Hata: ChromeDriver version mismatch
# Çözüm: Chrome güncellemesi sonrası driver güncelleyin
pip install --upgrade webdriver-manager
```

#### 2. API Key Hatası
```bash
# Hata: Gemini API key invalid
# Çözüm: .env dosyasında doğru key'i kontrol edin
GEMINI_API_KEY=AIzaSy...
```

#### 3. Port Çakışması
```bash
# Hata: Port already in use
# Çözüm: Farklı port kullanın
uvicorn main:app --port 8001
```

#### 4. Extension Çalışmıyor
- Browser'ı yeniden başlatın
- Extension'ı yeniden yükleyin
- Server'ın çalıştığını kontrol edin

### Debug Komutları

```bash
# Server durumu kontrolü
curl http://127.0.0.1:8001/status

# Cache durumu
cat analyze_cache.json

# Log kontrolü
tail -f server.log
```

## 🤝 Katkıda Bulunma

### Geliştirme Süreci

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları

- Python: PEP 8 standartları
- JavaScript: ES6+ syntax
- Commit messages: Conventional Commits formatı
- Docstring: Google style

### Yeni Veri Kaynağı Ekleme

1. `services/` klasörüne yeni modül ekleyin
2. `routers/analyze.py`'de servisi entegre edin
3. Cache mekanizmasını güncelleyin
4. Test edin




## 👥 Ekip

- **Geliştirici**: HilalNurGedikli, nslzsn, batoddy
- **AI Entegrasyon**: Google Gemini
- **Veri Kaynakları**: Şikayetvar, Ekşi Sözlük, Sosyal Medya

## 📞 İletişim

- **GitHub**: [@HilalNurGedikli](https://github.com/HilalNurGedikli)
- **Proje Linki**: [Elalem Ne Diyor Project](https://github.com/HilalNurGedikli/Elalem_Ne_Diyor_Project)

---

<div align="center">

**🔍 Elalem Ne Diyor - Akıllı E-ticaret Analiz Platformu**

![Made with ❤️ in Turkey](https://img.shields.io/badge/Made%20with%20❤️-in%20Turkey-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow)

</div>
