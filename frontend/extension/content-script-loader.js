(function() {
    // Load the analytics script first
    const analyticsScript = document.createElement('script');
    analyticsScript.src = chrome.runtime.getURL('frontend/extension/analytics/analytics.js');
    analyticsScript.type = 'text/javascript';
    analyticsScript.onload = function() {
        console.log("Analytics script loaded");
    };
    (document.head || document.documentElement).appendChild(analyticsScript);

    // Load the content script after analytics is loaded
    analyticsScript.onload = function() {
        const contentScript = document.createElement('script');
        contentScript.src = chrome.runtime.getURL('frontend/extension/user/content.js');
        contentScript.type = 'module';
        (document.head || document.documentElement).appendChild(contentScript);
    };
})();
