# Elalem Ne Diyor - VS Code Extension

Bu VS Code extension'ı, web sitelerindeki kullanıcı yorumlarını analiz etmek için geliştirilmiştir.

## Özellikler

- 🌐 **Çoklu Site Desteği**: Şikayetvar, Ekşi Sözlük, Instagram, Twitter, Trendyol
- 🤖 **AI Analizi**: Gemini AI ile duygusal analiz
- 📊 **Görsel Dashboard**: VS Code içinde analiz paneli
- 📈 **Raporlama**: JSON ve TXT formatında detaylı raporlar
- ⚡ **Hızlı Analiz**: Tek tıkla site analizi

## Kurulum

1. Extension'ı VS Code'da aktif edin
2. Python sanal ortamınızın hazır olduğundan emin olun (`venv2` klasörü)
3. Gerekli Python paketlerinin yüklü olduğunu kontrol edin

## Kullanım

### Yeni Site Analizi
1. Command Palette'i açın (`Ctrl+Shift+P`)
2. "Elalem: Site Analizi Başlat" komutunu çalıştırın
3. Analiz edilecek site URL'sini girin
4. Sonuçları bekleyin

### Dashboard
- Extension aktif olduğunda otomatik olarak dashboard açılır
- "Elalem: Analiz Panelini Aç" komutu ile manuel açabilirsiniz

### Sonuçları Görüntüleme
- "Elalem: Sonuçları Görüntüle" komutu ile sonuçları görüntüleyebilirsiniz

## Desteklenen Siteler

- **Şikayetvar.com**: Şikayet ve yorumları analiz eder
- **Ekşi Sözlük**: Entry'leri ve yorumları analiz eder
- **Instagram**: Post yorumlarını analiz eder
- **Twitter**: Tweet'leri ve yanıtları analiz eder
- **Trendyol**: Ürün yorumlarını analiz eder

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `elalem.analyzeSite` | Yeni site analizi başlatır |
| `elalem.openDashboard` | Analytics dashboard'unu açar |
| `elalem.viewResults` | Analiz sonuçlarını görüntüler |

## Geliştirme

```bash
# Bağımlılıkları yükle
npm install

# TypeScript derleme
npm run compile

# Watch mode
npm run watch
```

## Gereksinimler

- VS Code 1.74.0 veya üzeri
- Python 3.8+ (sanal ortam ile)
- Gerekli Python paketleri (requirements.txt'de listelenmiş)

## Lisans

MIT License
