console.log("%c--- CollegeBot Full-Stack API Configuration ---", "color: blue; font-weight: bold;");

// We use relative paths by pointing to the same origin. 
// This allows the frontend (Vercel) to talk to the backend (also on Vercel) seamlessly.
export const API_BASE_URL = window.location.origin;

console.log("Current API Base URL:", API_BASE_URL);
console.log("---------------------------------------");
