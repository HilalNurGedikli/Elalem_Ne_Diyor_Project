// Chrome Extension Popup Script

document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingDiv = document.getElementById('loading');
    
    // Loading göster
    loadingDiv.style.display = 'block';
    statusDiv.innerHTML = `
        <span class="icon">⏳</span>Extension yükleniyor...
    `;
    
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
            // Loading gizle
            loadingDiv.style.display = 'none';
            
            const siteInfo = results;
            
            // Platform mağazası mı kontrol et
            const isPlatformStore = siteInfo.isPlatformStore || false;
            const storeName = siteInfo.originalSiteName || siteInfo.siteName;
            const platformInfo = isPlatformStore ? ` (${siteInfo.platformDisplay} üzerinde)` : '';
            
            // Artık tüm siteler destekleniyor
            statusDiv.innerHTML = `
                <div style="color: #4CAF50; margin-bottom: 10px;">
                    <span class="icon">✅</span><strong>${storeName}${platformInfo}</strong>
                </div>
                <div style="margin-bottom: 8px;"><strong>Site:</strong> ${storeName}</div>
                <div style="margin-bottom: 8px;"><strong>URL:</strong> ${siteInfo.currentUrl}</div>
                <div style="margin-bottom: 8px;"><strong>Domain:</strong> ${siteInfo.simpleDomain}</div>
                ${isPlatformStore ? `<div style="margin-bottom: 8px;"><strong>Platform:</strong> ${siteInfo.platformDisplay}</div>` : ''}
                ${siteInfo.searchTerm ? `<div style="margin-bottom: 8px;"><strong>Arama:</strong> ${siteInfo.searchTerm}</div>` : ''}
                <div style="font-size: 12px; color: #666;">
                    <span class="icon">🔍</span>${isPlatformStore ? `Bu ${siteInfo.platformDisplay} mağazası analiz edilebilir.` : 'Bu site analiz edilebilir.'}
                </div>
            `;
            
            // Analiz butonunu aktif et ve site adını ekle
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = `<span class="icon">📊</span>${storeName} Analiz Et`;
            
            // Analiz butonuna click event ekle
            analyzeBtn.addEventListener('click', async () => {
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = `<span class="icon">⏳</span>Yeni sekmede açılıyor...`;
                loadingDiv.style.display = 'block';
                
                try {
                    console.log('🔍 Analiz başlatılıyor:', storeName);
                    
                    // İlk olarak analysis.html'i dene
                    const analysisUrl = chrome.runtime.getURL(`analysis.html?site=${encodeURIComponent(storeName)}`);
                    console.log('📍 Analysis URL:', analysisUrl);
                    
                    try {
                        await chrome.tabs.create({ url: analysisUrl });
                        console.log('✅ Yeni sekme açıldı');
                        
                        // Popup'ı kapat
                        window.close();
                        return; // Başarılı olursa burada çık
                    } catch (tabError) {
                        console.warn('⚠️ Analysis.html açılamadı, alternatif deneniyor:', tabError);
                        
                        // Alternatif: Basit HTML sayfası oluştur
                        const simpleAnalysisPage = `
                            <html>
                            <head><title>${storeName} Analizi</title></head>
                            <body style="font-family: Arial; padding: 20px; background: #f5f5f5;">
                                <h1>🔍 ${storeName} Analizi</h1>
                                <p>⏳ Analiz başlatılıyor...</p>
                                <script>
                                    setTimeout(() => {
                                        window.location.href = 'http://127.0.0.1:8003/analyze?site=${encodeURIComponent(storeName)}';
                                    }, 2000);
                                </script>
                            </body>
                            </html>
                        `;
                        
                        const dataUrl = 'data:text/html;charset=utf-8,' + encodeURIComponent(simpleAnalysisPage);
                        await chrome.tabs.create({ url: dataUrl });
                        console.log('✅ Alternatif sayfa açıldı');
                        
                        // Popup'ı kapat
                        window.close();
                        return;
                    }
                } catch (error) {
                    console.error('❌ Analiz sayfası açılamadı:', error);
                    loadingDiv.style.display = 'none';
                    analyzeBtn.disabled = false;
                    analyzeBtn.innerHTML = `<span class="icon">📊</span>${storeName} Analiz Et`;
                    
                    // Hata mesajını göster
                    statusDiv.innerHTML += `
                        <div style="background: #ffe8e8; color: #d32f2f; padding: 10px; 
                                    border-radius: 6px; margin-top: 10px; font-size: 12px;">
                            ❌ Analiz sayfası açılamadı: ${error.message}
                        </div>
                    `;
                    
                    // Hata durumunda eski yöntemi dene
                    try {
                        console.log('🔄 Fallback API denemesi...');
                        const response = await fetch(`http://127.0.0.1:8003/analyze?site=${encodeURIComponent(storeName)}`);
                        const data = await response.json();
                        
                        // Basit sonuç göster
                        statusDiv.innerHTML = `
                            <div style="color: #4CAF50; margin-bottom: 10px;">
                                <span class="icon">✅</span><strong>Analiz Tamamlandı</strong>
                            </div>
                            <div style="font-size: 12px;">
                                Yorum sayısı: ${data.yorum_sayısı || 0}<br>
                                ${data.analiz ? data.analiz.substring(0, 100) + '...' : 'Analiz bulunamadı'}
                            </div>
                        `;
                        console.log('✅ Fallback API başarılı');
                    } catch (fallbackError) {
                        console.error('❌ Fallback API de başarısız:', fallbackError);
                        statusDiv.innerHTML = `
                            <div style="color: #f44336;">
                                <span class="icon">❌</span><strong>Analiz Başarısız</strong><br>
                                <small>API sunucusu çalışmıyor olabilir.</small>
                            </div>
                        `;
                    }
                }
            });
        } else {
            // Loading gizle
            loadingDiv.style.display = 'none';
            
            statusDiv.innerHTML = `
                <div style="color: #f44336;">
                    <span class="icon">❌</span><strong>Site bilgisi alınamadı</strong>
                </div>
                <div style="font-size: 12px; color: #666; margin-top: 5px;">
                    <span class="icon">🔄</span>Sayfayı yenileyin ve tekrar deneyin.
                </div>
            `;
            analyzeBtn.disabled = true;
        }
        
    } catch (error) {
        // Loading gizle
        loadingDiv.style.display = 'none';
        
        console.error('Popup yüklenirken hata:', error);
        statusDiv.innerHTML = `
            <div style="color: #f44336;">
                <span class="icon">❌</span><strong>Extension yüklenemedi</strong>
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">
                <span class="icon">⚠️</span>${error.message}
            </div>
        `;
        analyzeBtn.disabled = true;
    }
    
    // Analysis sayfasını açma butonu
    setupAnalysisButton();
});

// Analysis sayfasını açma fonksiyonu
function setupAnalysisButton() {
    const openAnalysisBtn = document.getElementById('openAnalysisBtn');
    
    if (openAnalysisBtn) {
        openAnalysisBtn.addEventListener('click', function() {
            openAnalysisBtn.disabled = true;
            openAnalysisBtn.innerHTML = '<span class="icon">⏳</span>Analysis sayfası açılıyor...';
            
            try {
                console.log('🔍 Analysis sayfası açılıyor...');
                
                // Analysis.html sayfasını aç
                const analysisUrl = chrome.runtime.getURL('analysis.html');
                console.log('📍 Analysis URL:', analysisUrl);
                
                chrome.tabs.create({ url: analysisUrl }).then(() => {
                    console.log('✅ Analysis sayfası açıldı');
                    // Popup'ı kapat
                    window.close();
                }).catch((error) => {
                    console.error('❌ Analysis sayfası açılamadı:', error);
                    openAnalysisBtn.disabled = false;
                    openAnalysisBtn.innerHTML = '<span class="icon">🔍</span>Başka Bir Site Analiz Et';
                    
                    // Hata mesajı göster
                    const statusDiv = document.getElementById('status');
                    statusDiv.innerHTML += `
                        <div style="background: #ffe8e8; color: #d32f2f; padding: 10px; 
                                    border-radius: 6px; margin-top: 10px; font-size: 12px;">
                            ❌ Analysis sayfası açılamadı: ${error.message}
                        </div>
                    `;
                });
            } catch (error) {
                console.error('❌ Analysis sayfası açılamadı:', error);
                openAnalysisBtn.disabled = false;
                openAnalysisBtn.innerHTML = '<span class="icon">🔍</span>Başka Bir Site Analiz Et';
            }
        });
    }
}
