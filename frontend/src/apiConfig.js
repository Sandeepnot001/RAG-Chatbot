console.log("Environment:", import.meta.env.MODE);
const envApiUrl = import.meta.env.VITE_API_URL;
console.log("VITE_API_URL from env:", envApiUrl);

export const API_BASE_URL = envApiUrl || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '');

console.log("Resolved API_BASE_URL:", API_BASE_URL);

if (!API_BASE_URL) {
    console.error("CRITICAL error: API_BASE_URL is not set. API calls will fail.");
    if (import.meta.env.PROD) {
        console.warn("Please add VITE_API_URL to your Vercel Environment Variables.");
    }
}
