export const API_BASE_URL = import.meta.env.VITE_API_URL || '';

if (import.meta.env.PROD && !API_BASE_URL) {
    console.warn("VITE_API_URL is not set. API calls will fail on Vercel.");
}
