import { useState } from "react";
import { queryRag } from "../api/api";

export default function RagChat() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(false);

    async function askQuestion() {
        if (!question.trim()) return;

        setLoading(true);
        setAnswer("");

        try {
            const res = await queryRag(question);
            setAnswer(res.answer);
            setSources(res.sources || []);
        } catch {
            setAnswer("Error querying RAG.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h3>Chat</h3>

            <textarea
                className="input"
                rows={3}
                placeholder="Ask a research question…"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />

            <button className="primary-btn" onClick={askQuestion} disabled={loading}>
                {loading ? "Thinking…" : "Ask"}
            </button>

            {answer && (
                <div className="answer-box">
                    <strong>Answer</strong>
                    <p>{answer}</p>
                </div>
            )}
            {sources.length > 0 && (
                <div className="sources-box">
                    <strong>Sources</strong>
                    <ul>
                        {[
                            ...new Set(
                                sources.map((src) => {
                                    const sourcePath =
                                        src.metadata?.source ||
                                        src.metadata?.file_name ||
                                        src.metadata?.filename ||
                                        "";

                                    return sourcePath
                                        .split("/")
                                        .pop()
                                        .split("\\")
                                        .pop();
                                })
                            ),
                        ].map((fileName, idx) => (
                            <li key={idx}>{fileName || "Unknown file"}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
