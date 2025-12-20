import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { verifyMagicLink } from "../api/api";

export default function MagicLogin() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const [status, setStatus] = useState("verifying"); // verifying | error
    const [error, setError] = useState("");

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
                localStorage.setItem("token", res.access_token);
                // FORCE full reload so App reloads user
                window.location.href = "/";
            } catch (err) {
                setStatus("error");
                setError(err.message);
            }
        }

        verify();
    }, [searchParams, navigate]);

    if (status === "verifying") {
        return (
            <div className="center">
                <h2>Verifying magic link…</h2>
                <p className="muted">Please wait</p>
            </div>
        );
    }

    return (
        <div className="center">
            <h2>Magic Link Error</h2>
            <p className="error">{error}</p>
        </div>
    );
}
