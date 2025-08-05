// Background script - Extension'ın arka plan servisi
console.log('Elalem Ne Diyor background script başlatıldı');

// Extension kurulduğunda
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('Elalem Ne Diyor extension kuruldu');
        
        // Hoş geldin sekmesi aç
        chrome.tabs.create({
            url: chrome.runtime.getURL('welcome.html')
        });
    }
});

// Tab güncellendiğinde kontrol et
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        checkSiteSupport(tab);
    }
});

// Site desteği kontrolü
function checkSiteSupport(tab) {
    const supportedSites = [
        'www.sikayetvar.com',
        'eksisozluk.com',
        'www.instagram.com',
        'twitter.com',
        'www.trendyol.com'
    ];

    try {
        const url = new URL(tab.url);
        const hostname = url.hostname;
        
        if (supportedSites.includes(hostname)) {
            // Badge göster
            chrome.action.setBadgeText({
                tabId: tab.id,
                text: '✓'
            });
            
            chrome.action.setBadgeBackgroundColor({
                tabId: tab.id,
                color: '#4CAF50'
            });
            
            // Tooltip güncelle
            chrome.action.setTitle({
                tabId: tab.id,
                title: 'Elalem Ne Diyor - Bu site destekleniyor! 🎉'
            });
        } else {
            // Badge temizle
            chrome.action.setBadgeText({
                tabId: tab.id,
                text: ''
            });
            
            chrome.action.setTitle({
                tabId: tab.id,
                title: 'Elalem Ne Diyor - Site Analytics'
            });
        }
    } catch (error) {
        console.error('URL parsing error:', error);
    }
}

// Context menu (sağ tık menüsü) ekle
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: 'analyzePage',
        title: '🔍 Bu sayfayı Elalem ile analiz et',
        contexts: ['page']
    });
});

// Context menu tıklanınca
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'analyzePage') {
        // Content script'e analiz başlat mesajı gönder
        chrome.tabs.sendMessage(tab.id, {
            action: 'startAnalysis',
            url: tab.url
        });
    }
});

// Mesaj dinleyicisi
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'saveAnalysis') {
        // Analiz sonucunu kaydet
        saveAnalysisResult(request.data)
            .then(() => {
                sendResponse({ success: true });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true;
    }
    
    if (request.action === 'getAnalysisHistory') {
        // Analiz geçmişini getir
        getAnalysisHistory()
            .then(history => {
                sendResponse({ success: true, data: history });
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true;
    }
});

// Analiz sonucunu storage'a kaydet
async function saveAnalysisResult(data) {
    try {
        const result = {
            ...data,
            timestamp: Date.now(),
            id: generateId()
        };

        const storage = await chrome.storage.local.get(['analysisResults']);
        const results = storage.analysisResults || [];
        
        results.unshift(result);
        
        // Maksimum 100 sonuç sakla
        if (results.length > 100) {
            results.splice(100);
        }

        await chrome.storage.local.set({ analysisResults: results });
        console.log('Analiz sonucu kaydedildi:', result.id);
    } catch (error) {
        console.error('Analiz sonucu kaydetme hatası:', error);
        throw error;
    }
}

// Analiz geçmişini getir
async function getAnalysisHistory() {
    try {
        const storage = await chrome.storage.local.get(['analysisResults']);
        return storage.analysisResults || [];
    } catch (error) {
        console.error('Analiz geçmişi getirme hatası:', error);
        throw error;
    }
}

// Unique ID generator
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Periodic cleanup - Eski sonuçları temizle
setInterval(async () => {
    try {
        const storage = await chrome.storage.local.get(['analysisResults']);
        const results = storage.analysisResults || [];
        
        // 30 günden eski sonuçları sil
        const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
        const filteredResults = results.filter(result => result.timestamp > thirtyDaysAgo);
        
        if (filteredResults.length !== results.length) {
            await chrome.storage.local.set({ analysisResults: filteredResults });
            console.log(`${results.length - filteredResults.length} eski analiz sonucu temizlendi`);
        }
    } catch (error) {
        console.error('Cleanup hatası:', error);
    }
}, 24 * 60 * 60 * 1000); // 24 saatte bir çalıştır
