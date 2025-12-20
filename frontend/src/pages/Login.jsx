import { useState } from "react";
import { login, requestMagicLink } from "../api/api";
import "../styles/Login.css";

export default function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [msg, setMsg] = useState("");
    const [loading, setLoading] = useState(false);
    const [showMagic, setShowMagic] = useState(false);

    /* ---------------- PASSWORD LOGIN ---------------- */
    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setMsg("");
        setLoading(true);

        try {
            const res = await login(email, password);
            localStorage.setItem("token", res.access_token);
            onLogin();
        } catch {
            setError("Invalid credentials");
        } finally {
            setLoading(false);
        }
    }

    /* ---------------- MAGIC LINK LOGIN ---------------- */
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

            {/* -------- PASSWORD LOGIN -------- */}
            {!showMagic && (
                <>
                    <form onSubmit={handleSubmit}>
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />

                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        <button type="submit" disabled={loading}>
                            {loading ? "Logging in..." : "Login"}
                        </button>
                    </form>

                    <p
                        className="link subtle"
                        onClick={() => {
                            setShowMagic(true);
                            setError("");
                            setMsg("");
                        }}
                    >
                        Forgot password?
                    </p>
                </>
            )}

            {/* -------- MAGIC LINK LOGIN -------- */}
            {showMagic && (
                <>
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

                    <p
                        className="link subtle"
                        onClick={() => {
                            setShowMagic(false);
                            setError("");
                            setMsg("");
                        }}
                    >
                        ← Back to password login
                    </p>
                </>
            )}
        </div>
    );
}
