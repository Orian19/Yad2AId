(function() {
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('frontend/extension/user/content.js');
    script.type = 'module';
    (document.head || document.documentElement).appendChild(script);
})();
