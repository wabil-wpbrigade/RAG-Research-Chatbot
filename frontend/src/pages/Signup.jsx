import { useState } from "react";
import { signup } from "../api/api";

export default function Signup({ onDone }) {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function submit(e) {
        e.preventDefault();
        setError("");

        try {
            await signup(name, email, password);
            onDone();
        } catch {
            setError("Signup failed");
        }
    }

    return (
        <form className="card" onSubmit={submit}>
            <h2>Create Account</h2>

            {error && <p className="error">{error}</p>}

            <input
                placeholder="Full Name"
                value={name}
                onChange={e => setName(e.target.value)}
            />

            <input
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />

            <button>Create Account</button>
        </form>
    );
}
