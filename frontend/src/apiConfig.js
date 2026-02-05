console.log("Environment:", import.meta.env.MODE);
console.log("VITE_API_URL from env:", import.meta.env.VITE_API_URL);

export const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '');

console.log("Resolved API_BASE_URL:", API_BASE_URL);

if (import.meta.env.PROD && !API_BASE_URL) {
    console.warn("VITE_API_URL is not set. API calls will fail on Vercel.");
}
