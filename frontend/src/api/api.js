const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";



/**
 * Returns authorization headers using the stored JWT token.
 */
function authHeaders() {
    return { Authorization: `Bearer ${localStorage.getItem("token")}` };
}



/**
 * Performs a JSON fetch request and handles error responses.
 */
async function apiFetch(url, options, errorMsg) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(errorMsg || (await res.json()).detail);
    return res.json();
}



/**
 * Returns standard JSON headers.
 */
function jsonHeaders() {
    return { "Content-Type": "application/json" };
}



/**
 * Fetches the currently authenticated user.
 */
export function getMe() {
    return apiFetch(`${API_URL}/auth/me`, {
        headers: authHeaders(),
    }, "Unauthorized");
}



/**
 * Fetches all users (admin-only).
 */
export function fetchUsers() {
    return apiFetch(`${API_URL}/users`, {
        headers: authHeaders(),
    }, "Forbidden");
}



/**
 * Toggles a user's active status.
 */
export function toggleUserActive(token, userId) {
    return apiFetch(`${API_URL}/users/${userId}/active`, {
        method: "PATCH",
        headers: { ...jsonHeaders(), Authorization: `Bearer ${token}` },
    }, "Failed to update");
}



/**
 * Sends a question to the RAG system.
 */
export function queryRag(question) {
    return apiFetch(`${API_URL}/rag/query`, {
        method: "POST",
        headers: { ...jsonHeaders(), ...authHeaders() },
        body: JSON.stringify({ question }),
    }, "RAG query failed");
}



/**
 * Creates a new user account.
 */
export function signup(name, email, password) {
    return apiFetch(`${API_URL}/auth/signup`, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({ name, email, password }),
    }, "Signup failed");
}



/**
 * Creates a user or admin (admin-only).
 */
export function createUser(name, email, password, isAdmin) {
    return apiFetch(`${API_URL}/users`, {
        method: "POST",
        headers: { ...jsonHeaders(), ...authHeaders() },
        body: JSON.stringify({ name, email, password, is_admin: isAdmin }),
    }, "Create user failed");
}



/**
 * Requests a magic login link.
 */
export function requestMagicLink(email) {
    return apiFetch(`${API_URL}/auth/magic/request`, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({ email }),
    }, "Failed to send magic link");
}



/**
 * Verifies a magic login token and returns a JWT.
 */
export function verifyMagicLink(token) {
    return apiFetch(`${API_URL}/auth/magic/verify`, {
        method: "POST",
        headers: jsonHeaders(),
        body: JSON.stringify({ token }),
    }, "Magic link verification failed");
}
