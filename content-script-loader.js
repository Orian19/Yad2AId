(function() {
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('content.js');
    script.type = 'module';
    (document.head || document.documentElement).appendChild(script);
})();