// Chrome Extension Popup Script

document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    try {
        // Aktif tab'ı al
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        
        // Content script'i inject et
        await chrome.scripting.executeScript({
            target: {tabId: tab.id},
            files: ['content.js']
        });
        
        // Site bilgilerini al
        const results = await chrome.tabs.sendMessage(tab.id, {action: 'getSiteInfo'});
        
        if (results) {
            const siteInfo = results;
            
            // Platform mağazası mı kontrol et
            const isPlatformStore = siteInfo.isPlatformStore || false;
            const storeName = siteInfo.originalSiteName || siteInfo.siteName;
            const platformInfo = isPlatformStore ? ` (${siteInfo.platformDisplay} üzerinde)` : '';
            
            // Artık tüm siteler destekleniyor
            statusDiv.innerHTML = `
                <div style="color: #4CAF50; margin-bottom: 10px;">
                    <strong>✅ ${storeName}${platformInfo}</strong>
                </div>
                <div style="margin-bottom: 8px;"><strong>Site:</strong> ${storeName}</div>
                <div style="margin-bottom: 8px;"><strong>URL:</strong> ${siteInfo.currentUrl}</div>
                <div style="margin-bottom: 8px;"><strong>Domain:</strong> ${siteInfo.simpleDomain}</div>
                ${isPlatformStore ? `<div style="margin-bottom: 8px;"><strong>Platform:</strong> ${siteInfo.platformDisplay}</div>` : ''}
                ${siteInfo.searchTerm ? `<div style="margin-bottom: 8px;"><strong>Arama:</strong> ${siteInfo.searchTerm}</div>` : ''}
                <div style="font-size: 12px; color: #666;">
                    ${isPlatformStore ? `Bu ${siteInfo.platformDisplay} mağazası analiz edilebilir.` : 'Bu site analiz edilebilir.'}
                </div>
            `;
            
            // Analiz butonunu aktif et ve site adını ekle
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = `${storeName} Analiz Et`;
            
            // Analiz butonuna click event ekle
            analyzeBtn.addEventListener('click', async () => {
                analyzeBtn.disabled = true;
                analyzeBtn.textContent = 'Analiz ediliyor...';
                
                try {
                    // Platform mağazası ise mağaza ismini kullan
                    const analyzeTarget = isPlatformStore ? storeName : siteInfo.siteName;
                    
                    // Analiz isteği gönder
                    await chrome.tabs.sendMessage(tab.id, {action: 'analyzeSite', storeName: analyzeTarget});
                    
                    // Başarı mesajı göster
                    statusDiv.innerHTML += `
                        <div style="background: #e8f5e8; color: #2e7d2e; padding: 10px; 
                                    border-radius: 6px; margin-top: 10px; font-size: 14px;">
                            ✅ ${analyzeTarget} analiz talebi gönderildi! Sonuçlar sayfada görüntülenecek.
                        </div>
                    `;
                    
                    // Butonu yeniden aktif et
                    setTimeout(() => {
                        analyzeBtn.disabled = false;
                        analyzeBtn.textContent = `${storeName} Analiz Et`;
                    }, 3000);
                    
                } catch (error) {
                    console.error('Analiz hatası:', error);
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = `${storeName} Analiz Et`;
                    
                    statusDiv.innerHTML += `
                        <div style="background: #ffe8e8; color: #d32f2f; padding: 10px; 
                                    border-radius: 6px; margin-top: 10px; font-size: 14px;">
                            ❌ Analiz sırasında hata oluştu.
                        </div>
                    `;
                }
            });
        } else {
            statusDiv.innerHTML = `
                <div style="color: #f44336;">
                    <strong>❌ Site bilgisi alınamadı</strong>
                </div>
                <div style="font-size: 12px; color: #666; margin-top: 5px;">
                    Sayfayı yenileyin ve tekrar deneyin.
                </div>
            `;
            analyzeBtn.disabled = true;
        }
        
    } catch (error) {
        console.error('Popup yüklenirken hata:', error);
        statusDiv.innerHTML = `
            <div style="color: #f44336;">
                <strong>❌ Extension yüklenemedi</strong>
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">
                ${error.message}
            </div>
        `;
        analyzeBtn.disabled = true;
    }
    
    // Site arama özelliği
    setupSiteSearch();
});

// Site arama fonksiyonları
function setupSiteSearch() {
    const searchInput = document.getElementById('siteSearch');
    const searchBtn = document.getElementById('searchBtn');
    const suggestionsDiv = document.getElementById('suggestions');
    
    let searchTimeout;
    
    // Arama input'unda değişiklik olduğunda
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            suggestionsDiv.style.display = 'none';
            return;
        }
        
        // Debounce: 300ms bekle
        searchTimeout = setTimeout(() => {
            searchSites(query);
        }, 300);
    });
    
    // Arama butonu
    searchBtn.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query) {
            analyzeSiteByName(query);
        }
    });
    
    // Enter tuşu ile arama
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query) {
                analyzeSiteByName(query);
            }
        }
    });
}

async function searchSites(query) {
    const suggestionsDiv = document.getElementById('suggestions');
    
    try {
        const response = await fetch(`http://127.0.0.1:8003/search-site?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.suggestions.length > 0) {
            let suggestionsHTML = '';
            
            data.suggestions.forEach(suggestion => {
                const confidence = Math.round(suggestion.confidence * 100);
                suggestionsHTML += `
                    <div class="suggestion" data-site="${suggestion.key}">
                        <strong>${suggestion.display}</strong>
                        <div style="font-size: 10px; opacity: 0.8;">
                            ${suggestion.type} • %${confidence} eşleşme
                        </div>
                    </div>
                `;
            });
            
            suggestionsDiv.innerHTML = suggestionsHTML;
            suggestionsDiv.style.display = 'block';
            
            // Öneri tıklama olayları
            suggestionsDiv.querySelectorAll('.suggestion').forEach(item => {
                item.addEventListener('click', function() {
                    const siteName = this.dataset.site;
                    const displayName = this.querySelector('strong').textContent;
                    
                    document.getElementById('siteSearch').value = displayName;
                    suggestionsDiv.style.display = 'none';
                    
                    analyzeSiteByName(siteName);
                });
            });
            
        } else {
            suggestionsDiv.innerHTML = `
                <div class="suggestion" style="opacity: 0.6;">
                    "${query}" için öneri bulunamadı
                </div>
            `;
            suggestionsDiv.style.display = 'block';
        }
        
    } catch (error) {
        console.error('Site arama hatası:', error);
        suggestionsDiv.style.display = 'none';
    }
}

async function analyzeSiteByName(siteName) {
    const searchBtn = document.getElementById('searchBtn');
    const statusDiv = document.getElementById('status');
    
    searchBtn.disabled = true;
    searchBtn.textContent = 'Analiz ediliyor...';
    
    try {
        // Fake URL oluştur
        const fakeUrl = `https://${siteName.toLowerCase()}.com`;
        
        // Analiz isteği
        const response = await fetch('http://127.0.0.1:8003/analyze-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: fakeUrl,
                site_type: 'generic',
                data: {
                    comments: [],
                    source: 'extension_search'
                }
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Başarı mesajı göster
            statusDiv.innerHTML += `
                <div style="background: #e8f5e8; color: #2e7d2e; padding: 10px; 
                            border-radius: 6px; margin-top: 10px; font-size: 12px;">
                    ✅ ${siteName} analizi tamamlandı!<br>
                    <small>Sonuçlar: ${result.data?.main_analysis?.yorum_sayısı || 0} yorum analiz edildi</small>
                </div>
            `;
            
            // Yeni tab'da sonuçları göster
            const resultsUrl = `data:text/html;charset=utf-8,${encodeURIComponent(generateResultsHTML(result))}`;
            chrome.tabs.create({ url: resultsUrl });
            
        } else {
            throw new Error('API yanıt vermedi');
        }
        
    } catch (error) {
        console.error('Site analiz hatası:', error);
        statusDiv.innerHTML += `
            <div style="background: #ffe8e8; color: #d32f2f; padding: 10px; 
                        border-radius: 6px; margin-top: 10px; font-size: 12px;">
                ❌ ${siteName} analizi başarısız: ${error.message}
            </div>
        `;
    } finally {
        searchBtn.disabled = false;
        searchBtn.textContent = 'Ara & Analiz Et';
        document.getElementById('suggestions').style.display = 'none';
    }
}

function generateResultsHTML(result) {
    const analysis = result.data?.main_analysis || {};
    const siteName = analysis.site || 'Bilinmeyen Site';
    const commentCount = analysis.yorum_sayısı || 0;
    const analysisText = analysis.analiz || 'Analiz yapılamadı';
    
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>${siteName} - Analiz Sonuçları</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .stats { background: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
                .analysis { background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px; line-height: 1.6; }
                .copy-btn { background: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌐 ${siteName} - Analiz Sonuçları</h1>
                <p>Elalem Analytics tarafından oluşturuldu</p>
            </div>
            
            <div class="stats">
                <h3>📊 İstatistikler</h3>
                <p><strong>Analiz edilen yorum sayısı:</strong> ${commentCount}</p>
                <p><strong>Analiz tarihi:</strong> ${new Date().toLocaleString('tr-TR')}</p>
            </div>
            
            <div class="analysis">
                <h3>🔍 Detaylı Analiz</h3>
                <div id="analysisContent">${analysisText.replace(/\n/g, '<br>')}</div>
                
                <button class="copy-btn" onclick="copyAnalysis()">📋 Analizi Kopyala</button>
                <button class="copy-btn" onclick="copyJSON()">📄 JSON Kopyala</button>
            </div>
            
            <script>
                function copyAnalysis() {
                    const text = \`${analysisText}\`;
                    navigator.clipboard.writeText(text).then(() => {
                        alert('Analiz kopyalandı!');
                    });
                }
                
                function copyJSON() {
                    const data = ${JSON.stringify(result, null, 2)};
                    navigator.clipboard.writeText(JSON.stringify(data, null, 2)).then(() => {
                        alert('JSON verisi kopyalandı!');
                    });
                }
            </script>
        </body>
        </html>
    `;
}
