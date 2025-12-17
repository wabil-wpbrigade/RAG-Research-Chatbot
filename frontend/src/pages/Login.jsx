import { useState } from "react";
import { login } from "../api/api";
import "../styles/Login.css";

export default function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");

        try {
            const res = await login(email, password);
            localStorage.setItem("token", res.access_token);
            onLogin();
        } catch {
            setError("Invalid credentials");
        }
    }

    return (
        <form className="card" onSubmit={handleSubmit}>
            <h2>Sign In</h2>

            {error && <p className="error">{error}</p>}

            <input
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

            <button type="submit">Login</button>
        </form>
    );
}
