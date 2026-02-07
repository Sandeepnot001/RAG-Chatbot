console.log("%c--- CollegeBot Localhost API Configuration ---", "color: blue; font-weight: bold;");

// In purely local mode, we always point to the local FastAPI server
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

console.log("Local API URL being used:", API_BASE_URL);
console.log("---------------------------------------");
