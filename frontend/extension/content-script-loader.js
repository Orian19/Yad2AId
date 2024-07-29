(function() {
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('frontend/extension/content.js'); // Ensure this path matches the actual location
    script.type = 'module';
    (document.head || document.documentElement).appendChild(script);
})();
