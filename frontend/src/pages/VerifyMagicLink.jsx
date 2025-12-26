import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { verifyMagicLink } from "../api/api";

/**
 * MagicLogin Component
 *
 * Handles passwordless authentication via magic link.
 *
 * Flow:
 * 1. Reads the `token` from URL query parameters
 * 2. Verifies the token with the backend
 * 3. Stores the returned JWT on success
 * 4. Forces a full app reload to rehydrate auth state
 *
 * States:
 * - verifying: Token verification in progress
 * - error: Verification failed or token missing
 */
export default function VerifyMagicLink() {
    /** URL query parameters (expects ?token=...) */
    const [searchParams] = useSearchParams();

    /** Router navigation helper (kept for extensibility) */
    const navigate = useNavigate();

    /** Current verification status */
    const [status, setStatus] = useState("verifying"); // verifying | error

    /** Error message shown on failure */
    const [error, setError] = useState("");

    /**
     * Verify magic link token on page load.
     *
     * - If token is missing → show error
     * - If verification succeeds → store JWT + reload app
     * - If verification fails → show error
     */
    useEffect(() => {
        const token = searchParams.get("token");

        if (!token) {
            setStatus("error");
            setError("Missing magic link token");
            return;
        }

        async function verify() {
            try {
                const res = await verifyMagicLink(token);

                // Persist JWT for authenticated requests
                localStorage.setItem("token", res.access_token);

                // Force full reload so App re-fetches user state
                window.location.href = "/";
            } catch (err) {
                setStatus("error");
                setError(err.message || "Magic link verification failed");
            }
        }

        verify();
    }, [searchParams, navigate]);

    /* ---------------- LOADING STATE ---------------- */
    if (status === "verifying") {
        return (
            <div className="center">
                <h2>Verifying magic link…</h2>
                <p className="muted">Please wait</p>
            </div>
        );
    }

    /* ---------------- ERROR STATE ---------------- */
    return (
        <div className="center">
            <h2>Magic Link Error</h2>
            <p className="error">{error}</p>
        </div>
    );
}
