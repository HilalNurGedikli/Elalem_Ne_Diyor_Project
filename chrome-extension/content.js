// Content script - Web sayfasında çalışır
console.log('Elalem Ne Diyor content script yüklendi');

// Sayfadaki yorumları ve içeriği analiz etmek için kullanılacak
class ElalemAnalyzer {
    constructor() {
        this.comments = [];
        this.siteInfo = {};
        this.init();
    }

    init() {
        this.detectSiteType();
        this.addAnalysisButton();
    }

    detectSiteType() {
        const hostname = window.location.hostname.toLowerCase();
        
        // Artık tüm siteler destekleniyor, sadece türünü belirle
        if (hostname.includes('sikayetvar.com')) {
            this.siteType = 'sikayetvar';
            this.siteName = 'Şikayetvar';
        } else if (hostname.includes('eksisozluk.com') || hostname.includes('ekşisözlük.com')) {
            this.siteType = 'eksisozluk';
            this.siteName = 'Ekşi Sözlük';
        } else if (hostname.includes('instagram.com')) {
            this.siteType = 'instagram';
            this.siteName = 'Instagram';
        } else if (hostname.includes('twitter.com') || hostname.includes('x.com')) {
            this.siteType = 'twitter';
            this.siteName = 'Twitter';
        } else if (hostname.includes('trendyol.com')) {
            this.siteType = 'trendyol';
            this.siteName = 'Trendyol';
        } else {
            // Tüm diğer siteler için genel analiz
            this.siteType = 'generic';
            this.siteName = this.getDisplayName(hostname);
        }
        
        // Site bilgilerini object olarak sakla
        this.siteInfo = {
            siteName: this.siteName,
            siteType: this.siteType,
            hostname: hostname,
            url: window.location.href,
            title: document.title,
            timestamp: new Date().toISOString()
        };
    }

    getSiteInfo() {
        // Site bilgilerini güncel halde döndür
        const hostname = window.location.hostname.toLowerCase();
        const simpleDomain = this.getSimpleDomain(hostname);
        const displayName = this.getDisplayName(hostname);
        
        return {
            siteName: displayName,
            siteType: this.siteType || 'generic',
            hostname: hostname,
            simpleDomain: simpleDomain,
            currentUrl: window.location.href,
            url: window.location.href,
            title: document.title,
            timestamp: new Date().toISOString(),
            isSupported: true, // Artık tüm siteler destekleniyor
            searchTerm: this.extractSearchTerm()
        };
    }
    
    getDisplayName(hostname) {
        // Hostname'den güzel görünen isim oluştur
        const simpleDomain = this.getSimpleDomain(hostname);
        
        // Bilinen siteler için özel isimler
        const knownSites = {
            'sikayetvar': 'Şikayetvar',
            'eksisozluk': 'Ekşi Sözlük',
            'trendyol': 'Trendyol',
            'instagram': 'Instagram',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'youtube': 'YouTube',
            'google': 'Google',
            'amazon': 'Amazon',
            'netflix': 'Netflix',
            'spotify': 'Spotify',
            'linkedin': 'LinkedIn',
            'github': 'GitHub',
            'stackoverflow': 'Stack Overflow',
            'reddit': 'Reddit'
        };
        
        return knownSites[simpleDomain] || simpleDomain.charAt(0).toUpperCase() + simpleDomain.slice(1);
    }
    
    extractSearchTerm() {
        // URL'den arama terimini çıkarmaya çalış
        const url = window.location.href;
        const urlParams = new URLSearchParams(window.location.search);
        
        // Yaygın arama parametreleri
        const searchParams = ['q', 'query', 'search', 's', 'term', 'keyword'];
        
        for (const param of searchParams) {
            if (urlParams.has(param)) {
                return urlParams.get(param);
            }
        }
        
        // URL path'inde arama terimi olabilir
        const pathParts = window.location.pathname.split('/').filter(part => part.length > 0);
        if (pathParts.length > 0) {
            return pathParts[pathParts.length - 1].replace(/[-_]/g, ' ');
        }
        
        return null;
    }

    getSimpleDomain(hostname) {
        // www.sikayetvar.com -> sikayetvar
        // eksisozluk.com -> eksisozluk  
        // m.trendyol.com -> trendyol
        
        let domain = hostname.toLowerCase();
        
        // www. kaldır
        if (domain.startsWith('www.')) {
            domain = domain.substring(4);
        }
        
        // m. kaldır (mobil)
        if (domain.startsWith('m.')) {
            domain = domain.substring(2);
        }
        
        // .com, .net, .org vb. kaldır
        const parts = domain.split('.');
        if (parts.length > 1) {
            // İlk kısmı al (örn: sikayetvar.com -> sikayetvar)
            return parts[0];
        }
        
        return domain;
    }

    addAnalysisButton() {
        // Sayfaya analiz butonu ekle
        const button = document.createElement('div');
        button.id = 'elalem-analysis-btn';
        button.innerHTML = '🔍 Elalem Analizi';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            border: none;
        `;

        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.05)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });

        button.addEventListener('click', () => {
            this.startQuickAnalysis();
        });

        document.body.appendChild(button);
    }

    async startQuickAnalysis() {
        const button = document.getElementById('elalem-analysis-btn');
        button.innerHTML = '⏳ Analiz Ediliyor...';
        button.style.pointerEvents = 'none';

        try {
            // Önce API test et
            const testResponse = await fetch('http://127.0.0.1:8000/test');
            if (!testResponse.ok) {
                throw new Error('API server ulaşılamıyor');
            }
            console.log('✅ API Test başarılı');
            
            const data = await this.extractData();
            
            // Başarı mesajı göster
            this.showNotification('✅ Analiz tamamlandı!', 'success');
            
            // Python API'sine veri gönder (eğer local server çalışıyorsa)
            await this.sendToPythonAPI(data);
            
        } catch (error) {
            console.error('Analiz hatası:', error);
            this.showNotification('❌ Analiz hatası: ' + error.message, 'error');
        } finally {
            button.innerHTML = '🔍 Elalem Analizi';
            button.style.pointerEvents = 'auto';
        }
    }

    async extractData() {
        let data = {
            url: window.location.href,
            siteType: this.siteType,
            timestamp: new Date().toISOString(),
            comments: [],
            metadata: {}
        };

        switch (this.siteType) {
            case 'sikayetvar':
                data = await this.extractSikayetvarData();
                break;
            case 'eksisozluk':
                data = await this.extractEksisozlukData();
                break;
            case 'instagram':
                data = await this.extractInstagramData();
                break;
            case 'twitter':
                data = await this.extractTwitterData();
                break;
            case 'trendyol':
                data = await this.extractTrendyolData();
                break;
            case 'generic':
            default:
                // Tüm diğer siteler için genel veri toplama
                data = await this.extractGenericData();
                break;
        }

        return data;
    }
    
    async extractGenericData() {
        const comments = [];
        
        // Genel site için yaygın yorum/içerik selektorları
        const commentSelectors = [
            '.comment', '.comments', '.review', '.reviews',
            '.feedback', '.testimonial', '.post', '.content',
            'article', '.article', 'p', '.text', '.description'
        ];
        
        let foundComments = 0;
        for (const selector of commentSelectors) {
            const elements = document.querySelectorAll(selector);
            elements.forEach((element, index) => {
                const text = element.textContent.trim();
                if (text && text.length > 10 && foundComments < 50) { // En fazla 50 yorum al
                    comments.push({
                        id: foundComments,
                        text: text,
                        type: 'content',
                        selector: selector
                    });
                    foundComments++;
                }
            });
            
            if (foundComments >= 10) break; // Yeterli içerik bulunca dur
        }

        return {
            url: window.location.href,
            siteType: 'generic',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length,
                siteName: this.getDisplayName(window.location.hostname),
                pageTitle: document.title
            }
        };
    }

    async extractSikayetvarData() {
        const comments = [];
        
        // Şikayet metinlerini topla
        const complaintTexts = document.querySelectorAll('.complaint-text, .card-text, .complaint-content');
        complaintTexts.forEach((element, index) => {
            if (element.textContent.trim()) {
                comments.push({
                    id: index,
                    text: element.textContent.trim(),
                    type: 'complaint'
                });
            }
        });

        return {
            url: window.location.href,
            siteType: 'sikayetvar',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length,
                companyName: this.getCompanyNameFromURL()
            }
        };
    }

    async extractEksisozlukData() {
        const comments = [];
        
        // Entry'leri topla
        const entries = document.querySelectorAll('.content, .entry-text');
        entries.forEach((element, index) => {
            if (element.textContent.trim()) {
                comments.push({
                    id: index,
                    text: element.textContent.trim(),
                    type: 'entry'
                });
            }
        });

        return {
            url: window.location.href,
            siteType: 'eksisozluk',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length,
                topic: document.title
            }
        };
    }

    async extractInstagramData() {
        const comments = [];
        
        // Instagram yorumlarını topla (sınırlı - Instagram'ın anti-bot koruması var)
        const commentElements = document.querySelectorAll('[data-testid="comment"]');
        commentElements.forEach((element, index) => {
            const textElement = element.querySelector('span');
            if (textElement && textElement.textContent.trim()) {
                comments.push({
                    id: index,
                    text: textElement.textContent.trim(),
                    type: 'comment'
                });
            }
        });

        return {
            url: window.location.href,
            siteType: 'instagram',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length,
                postUrl: window.location.href
            }
        };
    }

    async extractTwitterData() {
        const comments = [];
        
        // Tweet'leri topla
        const tweets = document.querySelectorAll('[data-testid="tweet"]');
        tweets.forEach((element, index) => {
            const textElement = element.querySelector('[data-testid="tweetText"]');
            if (textElement && textElement.textContent.trim()) {
                comments.push({
                    id: index,
                    text: textElement.textContent.trim(),
                    type: 'tweet'
                });
            }
        });

        return {
            url: window.location.href,
            siteType: 'twitter',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length
            }
        };
    }

    async extractTrendyolData() {
        const comments = [];
        
        // Ürün yorumlarını topla
        const reviewElements = document.querySelectorAll('.comment-text, .review-text, .pr-rnr-c-review-text');
        reviewElements.forEach((element, index) => {
            if (element.textContent.trim()) {
                comments.push({
                    id: index,
                    text: element.textContent.trim(),
                    type: 'review'
                });
            }
        });

        return {
            url: window.location.href,
            siteType: 'trendyol',
            timestamp: new Date().toISOString(),
            comments: comments,
            metadata: {
                totalComments: comments.length,
                productName: document.querySelector('.pr-new-br')?.textContent || 'Bilinmiyor'
            }
        };
    }

    getCompanyNameFromURL() {
        const pathParts = window.location.pathname.split('/');
        return pathParts[1] || 'bilinmiyor';
    }

    async sendToPythonAPI(data) {
        try {
            // Site bilgilerini al
            const siteInfo = this.getSiteInfo();
            
            // Backend'in beklediği format
            const requestData = {
                url: siteInfo.currentUrl,
                site_type: siteInfo.siteType,
                data: data
            };
            
            console.log('API\'ye gönderilen veriler:', requestData);
            
            // Ana analiz endpoint'i (/analyze) - POST metodu ile
            const response = await fetch('http://127.0.0.1:8000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Analiz sonucu:', result);
                
                // Analiz sonucunu göster
                this.showAnalysisResults(result, siteInfo);
                this.showNotification(`✅ ${siteInfo.siteName} analizi tamamlandı!`, 'success');
                
                return result;
            } else {
                const errorText = await response.text();
                console.error('API Error:', response.status, errorText);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
        } catch (error) {
            console.log('API bağlantı hatası:', error);
            this.showNotification(`⚠️ API Hatası: ${error.message}`, 'warning');
            
            // Fallback: Extension'ın topladığı veriyi göster
            this.showLocalAnalysis(data);
        }
    }
    
    showAnalysisResults(analysisData, siteInfo) {
        // Ana analiz sonuçlarını sayfa üzerinde göster
        const resultDiv = document.createElement('div');
        resultDiv.id = 'elalem-analysis-results';
        
        // Analiz verisini formatla
        const yorumSayisi = analysisData.yorum_sayısı || analysisData.comment_count || 0;
        const analiz = analysisData.analiz || analysisData.analysis || 'Analiz bulunamadı';
        const siteName = analysisData.site || siteInfo?.siteName || 'Bilinmeyen Site';
        
        resultDiv.innerHTML = `
            <div style="position: fixed; top: 100px; right: 20px; z-index: 999999; 
                        background: white; color: #333; padding: 20px; border-radius: 12px; 
                        box-shadow: 0 8px 32px rgba(0,0,0,0.3); font-family: 'Segoe UI', Arial; 
                        max-width: 450px; border-left: 5px solid #4CAF50; max-height: 70vh; overflow-y: auto;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #4CAF50; font-size: 18px;">🎯 ${siteName} Analizi</h3>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                            style="background: #ff4444; color: white; border: none; border-radius: 50%; 
                                   width: 25px; height: 25px; cursor: pointer; font-size: 14px;">✕</button>
                </div>
                
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="margin-bottom: 8px;">
                        <strong>📊 Yorum Sayısı:</strong> <span style="color: #4CAF50; font-weight: bold;">${yorumSayisi}</span>
                    </div>
                    <div style="margin-bottom: 8px;">
                        <strong>🌐 Site:</strong> ${siteName}
                    </div>
                    <div style="font-size: 12px; color: #666;">
                        <strong>⏰ Analiz Zamanı:</strong> ${new Date().toLocaleString('tr-TR')}
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h4 style="margin: 0 0 10px 0; color: #333; font-size: 16px;">🤖 AI Analizi:</h4>
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; 
                                border-left: 4px solid #2196F3; line-height: 1.6; font-size: 14px;">
                        ${analiz.length > 500 ? analiz.substring(0, 500) + '...' : analiz}
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button onclick="window.open('http://127.0.0.1:8000/dashboard', '_blank')" 
                            style="flex: 1; background: #2196F3; color: white; border: none; padding: 10px; 
                                   border-radius: 6px; cursor: pointer; font-size: 13px;">
                        📋 Dashboard'u Aç
                    </button>
                    <button onclick="navigator.clipboard.writeText('${analiz.replace(/'/g, "\\'")}'); 
                                     this.textContent='✅ Kopyalandı'; setTimeout(() => this.textContent='📋 Kopyala', 2000)" 
                            style="background: #FF9800; color: white; border: none; padding: 10px; 
                                   border-radius: 6px; cursor: pointer; font-size: 13px;">
                        📋 Kopyala
                    </button>
                </div>
            </div>
        `;
        
        // Önceki sonuçları kaldır
        const existing = document.getElementById('elalem-analysis-results');
        if (existing) existing.remove();
        
        document.body.appendChild(resultDiv);
        
        // 30 saniye sonra otomatik kaldır
        setTimeout(() => {
            if (resultDiv.parentNode) {
                resultDiv.parentNode.removeChild(resultDiv);
            }
        }, 30000);
    }
    
    showLocalAnalysis(data) {
        // API çalışmadığında extension'ın topladığı veriyi göster
        const siteInfo = this.getSiteInfo();
        const yorumSayisi = data.comments ? data.comments.length : 0;
        
        const localResult = {
            site: siteInfo.siteName,
            yorum_sayısı: yorumSayisi,
            analiz: `Extension ${yorumSayisi} yorum topladı. Detaylı analiz için API server'ı başlatın.`
        };
        
        this.showAnalysisResults(localResult, siteInfo);
    }

    async sendToNativeHost(data) {
        return new Promise((resolve, reject) => {
            // Native messaging ile Python script'e bağlan
            const port = chrome.runtime.connectNative('com.elalem.analyzer');
            
            port.onMessage.addListener((response) => {
                if (response.success) {
                    resolve(response.data);
                } else {
                    reject(new Error(response.error));
                }
            });
            
            port.onDisconnect.addListener(() => {
                reject(new Error('Native host disconnected'));
            });
            
            // Analiz isteği gönder
            port.postMessage({
                action: 'analyze_site',
                url: data.url,
                siteType: data.siteType,
                data: data
            });
        });
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 10001;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            max-width: 300px;
        `;

        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #4CAF50, #45a049)';
        } else if (type === 'error') {
            notification.style.background = 'linear-gradient(135deg, #f44336, #da190b)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #2196F3, #1976D2)';
        }

        notification.textContent = message;
        document.body.appendChild(notification);

        // 3 saniye sonra kaldır
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Content script mesaj dinleyicisi
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getSiteInfo') {
        // Site bilgilerini popup'a gönder
        const analyzer = new ElalemAnalyzer();
        const siteInfo = analyzer.getSiteInfo();
        sendResponse(siteInfo);
        return true;
    }
    
    if (request.action === 'analyzeSite') {
        // Popup'tan analiz isteği geldiğinde
        const analyzer = new ElalemAnalyzer();
        analyzer.startQuickAnalysis()
            .then(() => {
                sendResponse({ success: true, message: 'Analiz başlatıldı' });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true; // Asenkron yanıt için
    }
    
    if (request.action === 'startAnalysis') {
        const analyzer = new ElalemAnalyzer();
        analyzer.extractData()
            .then(data => {
                sendResponse({ success: true, data: data });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true; // Asenkron yanıt için
    }
});

// Sayfa yüklendiğinde analyzer'ı başlat
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ElalemAnalyzer();
    });
} else {
    new ElalemAnalyzer();
}
