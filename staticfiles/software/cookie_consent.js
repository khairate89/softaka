// software/static/software/cookie_consent.js

document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookieConsentBanner');
    const acceptButton = document.getElementById('acceptCookies');
    const declineButton = document.getElementById('declineCookies');

    // Function to set a cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
    }

    // Function to get a cookie
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    // Function to erase a cookie (set expires to past)
    function eraseCookie(name) {   
        document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT; SameSite=Lax;';
    }

    // Check if the user has already made a choice
    const userConsent = getCookie('cookie_consent');

    if (!userConsent) {
        // If no choice, show the banner
        cookieBanner.style.display = 'block';
    } else if (userConsent === 'accepted') {
        // If accepted, load any non-essential scripts (e.g., Google Analytics)
        loadNonEssentialScripts();
    }
    // If 'declined', banner remains hidden and non-essential scripts are not loaded

    // Event listeners for buttons
    acceptButton.addEventListener('click', function() {
        setCookie('cookie_consent', 'accepted', 90); // Store consent for 90 days
        cookieBanner.style.display = 'none';
        loadNonEssentialScripts(); // Load scripts after acceptance
    });

    declineButton.addEventListener('click', function() {
        setCookie('cookie_consent', 'declined', 90); // Store decline for 90 days
        cookieBanner.style.display = 'none';
        // You might want to clear any existing non-essential cookies here if they were already set before explicit decline
        // For demonstration, we just prevent loading new ones.
        // If you had Google Analytics (without prior consent), you'd also need to stop it from tracking here.
    });

    // Function to dynamically load non-essential scripts
    function loadNonEssentialScripts() {
        // Example: Google Analytics
        // Replace 'YOUR_GA_TRACKING_ID' with your actual Google Analytics ID
        if (typeof window.ga === 'undefined' && !document.getElementById('google-analytics-script')) {
            const gaScript = document.createElement('script');
            gaScript.id = 'google-analytics-script';
            gaScript.async = true;
            gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX'; // Replace G-XXXXXXXXXX with your GA_MEASUREMENT_ID
            document.head.appendChild(gaScript);

            gaScript.onload = function() {
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'G-XXXXXXXXXX'); // Replace G-XXXXXXXXXX with your GA_MEASUREMENT_ID
            };
        }
        
        // Add other non-essential scripts here (e.g., Facebook Pixel, other tracking scripts)
    }
});