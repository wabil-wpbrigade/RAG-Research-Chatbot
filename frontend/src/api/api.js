const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";


/* ---------------- AUTH ---------------- */

export async function login(email, password) {
    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
        throw new Error("Login failed");
    }

    return res.json();
}

export async function getMe() {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/auth/me`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!res.ok) {
        throw new Error("Unauthorized");
    }

    return res.json();
}


/* ---------------- ADMIN ---------------- */

export async function fetchUsers() {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/users`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!res.ok) {
        throw new Error("Forbidden");
    }

    return res.json();
}

export async function toggleUserActive(token, userId) {
    const res = await fetch(
        `${API_URL}/users/${userId}/active`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        }
    );

    if (!res.ok) {
        throw new Error("Failed to update");
    }

    return res.json();
}



/* ---------------- RAG ---------------- */

export async function queryRag(question) {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/rag/query`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ question }),
    });

    if (!res.ok) {
        throw new Error("RAG query failed");
    }

    return res.json();
}


/* ---------------- NEW_USER ---------------- */

export async function signup(name, email, password) {
    const res = await fetch(`${API_URL}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) throw new Error("Signup failed");
    return res.json();
}

export async function createUser(name, email, password, isAdmin) {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API_URL}/users`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
            name,
            email,
            password,
            is_admin: isAdmin,
        }),
    });

    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Create user failed");
    }

    return res.json();
}



/* ---------------- MAGIC-LINK ---------------- */

export async function requestMagicLink(email) {
    const res = await fetch(`${API_URL}/auth/magic/request`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to send magic link");
    }

    return await res.json();
}

export async function verifyMagicLink(token) {
    const res = await fetch(`${API_URL}/auth/magic/verify`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
    });

    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Magic link verification failed");
    }

    return await res.json(); // returns JWT
}
