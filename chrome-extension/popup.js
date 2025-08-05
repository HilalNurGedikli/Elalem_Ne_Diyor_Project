// Chrome Extension Popup Script

document.addEventListener('DOMContentLoaded', async function() {
    const statusDiv = document.getElementById('status');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const dashboardBtn = document.getElementById('dashboardBtn');
    
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
            // Artık tüm siteler destekleniyor
            statusDiv.innerHTML = `
                <div style="color: #4CAF50; margin-bottom: 10px;">
                    <strong>✅ ${siteInfo.siteName}</strong>
                </div>
                <div style="margin-bottom: 8px;"><strong>Site:</strong> ${siteInfo.siteName}</div>
                <div style="margin-bottom: 8px;"><strong>URL:</strong> ${siteInfo.currentUrl}</div>
                <div style="margin-bottom: 8px;"><strong>Domain:</strong> ${siteInfo.simpleDomain}</div>
                ${siteInfo.searchTerm ? `<div style="margin-bottom: 8px;"><strong>Arama:</strong> ${siteInfo.searchTerm}</div>` : ''}
                <div style="font-size: 12px; color: #666;">Bu site analiz edilebilir.</div>
            `;
            
            // Analiz butonunu aktif et ve site adını ekle
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = `${siteInfo.siteName} Analiz Et`;
            
            // Analiz butonuna click event ekle
            analyzeBtn.addEventListener('click', async () => {
                analyzeBtn.disabled = true;
                analyzeBtn.textContent = 'Analiz ediliyor...';
                
                try {
                    // Analiz isteği gönder
                    await chrome.tabs.sendMessage(tab.id, {action: 'analyzeSite'});
                    
                    // Başarı mesajı göster
                    statusDiv.innerHTML += `
                        <div style="background: #e8f5e8; color: #2e7d2e; padding: 10px; 
                                    border-radius: 6px; margin-top: 10px; font-size: 14px;">
                            ✅ Analiz talebi gönderildi! Sonuçlar sayfada görüntülenecek.
                        </div>
                    `;
                    
                    // Butonu yeniden aktif et
                    setTimeout(() => {
                        analyzeBtn.disabled = false;
                        analyzeBtn.textContent = `${siteInfo.siteName} Analiz Et`;
                    }, 3000);
                    
                } catch (error) {
                    console.error('Analiz hatası:', error);
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = `${siteInfo.siteName} Analiz Et`;
                    
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
    
    // Dashboard butonu
    dashboardBtn.addEventListener('click', () => {
        chrome.tabs.create({url: 'http://127.0.0.1:8000/dashboard'});
        window.close();
    });
});
