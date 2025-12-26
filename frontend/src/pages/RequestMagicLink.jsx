import { useState } from "react";
import { requestMagicLink } from "../api/api";
import "../styles/MagicLinkLogin.css";

/**
 * Login Component
 *
 * Handles user authentication using:
 * 1. Traditional email + password login
 * 2. Passwordless magic link login
 *
 * Responsibilities:
 * - Manage login form state
 * - Call authentication APIs
 * - Store JWT token on successful login
 * - Toggle between password and magic-link flows
 */
export default function RequestMagicLink({ onLogin }) {
    /** User email input */
    const [email, setEmail] = useState("");

    /** Error message shown to the user */
    const [error, setError] = useState("");

    /** Success / informational message */
    const [msg, setMsg] = useState("");

    /** Loading state to prevent duplicate requests */
    const [loading, setLoading] = useState(false);

    /* ---------------- MAGIC LINK LOGIN ---------------- */

    /**
     * Requests a passwordless magic login link.
     *
     * - Validates email input
     * - Sends request to backend
     * - Displays success or error feedback
     */
    async function handleMagicLink() {
        if (!email) {
            setError("Please enter your email");
            return;
        }

        setError("");
        setMsg("");
        setLoading(true);

        try {
            await requestMagicLink(email);
            setMsg("Magic login link sent to your email.");
        } catch (err) {
            setError(err.message || "Failed to send magic link");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="card">
            <h2>Sign In</h2>

            {error && <p className="error">{error}</p>}
            {msg && <p className="success">{msg}</p>}

            <p className="muted">
                Enter your email and we’ll send you a secure login link.
            </p>

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <button onClick={handleMagicLink} disabled={loading}>
                {loading ? "Sending..." : "Send Magic Link"}
            </button>
        </div>
    );

}
