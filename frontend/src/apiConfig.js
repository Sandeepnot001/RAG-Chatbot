console.log("%c--- CollegeBot API Configuration ---", "color: blue; font-weight: bold;");
let envApiUrl = import.meta.env.VITE_API_URL;
console.log("Environment Variable (VITE_API_URL):", envApiUrl || "MISSING");

// 1. Auto-upgrade http to https if we are on a secure page (Vercel)
if (window.location.protocol === 'https:' && envApiUrl && envApiUrl.startsWith('http:')) {
    console.warn("⚠️ Protocol Mismatch: Upgrading VITE_API_URL to HTTPS to prevent blocking.");
    envApiUrl = envApiUrl.replace('http:', 'https:');
}

// 2. Resolve final API URL with fallback
// If VITE_API_URL is missing, we try a fallback. 
// NOTE: Users should set VITE_API_URL in Vercel Dashboard to their actual Render URL.
export const API_BASE_URL = envApiUrl || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : 'https://rag-chatbot-cocl.onrender.com');

console.log("Final API URL being used:", API_BASE_URL);

if (import.meta.env.PROD) {
    if (!envApiUrl) {
        console.warn("❗ VITE_API_URL is NOT set in Vercel. Using fallback: " + API_BASE_URL);
    }
    console.log("%c👉 To fix connection issues: Copy your 'onrender.com' URL from the Render Dashboard and add it to Vercel Environment Variables as VITE_API_URL.", "color: green;");
}
console.log("---------------------------------------");
