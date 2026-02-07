console.log("Environment:", import.meta.env.MODE);
let envApiUrl = import.meta.env.VITE_API_URL;
console.log("Original VITE_API_URL from env:", envApiUrl);

// 1. Auto-upgrade http to https if we are on a secure page (Vercel)
if (window.location.protocol === 'https:' && envApiUrl && envApiUrl.startsWith('http:')) {
    console.warn("Mixed Content Prevention: Upgrading VITE_API_URL to HTTPS");
    envApiUrl = envApiUrl.replace('http:', 'https:');
}

// 2. Resolve final API URL with fallback
export const API_BASE_URL = envApiUrl || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : 'https://rag-chatbot-backend.onrender.com');

console.log("Final Resolved API_BASE_URL:", API_BASE_URL);

if (!envApiUrl && import.meta.env.PROD) {
    console.warn("VITE_API_URL is missing. Using auto-fallback: " + API_BASE_URL);
}
