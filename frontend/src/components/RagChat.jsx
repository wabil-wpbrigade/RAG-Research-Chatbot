import { useState } from "react";
import { queryRag } from "../api/api";

/**
 * RagChat Component
 *
 * Provides a simple chat interface for querying a
 * Retrieval-Augmented Generation (RAG) backend.
 *
 * Responsibilities:
 * - Capture user question input
 * - Send query to RAG API
 * - Display the generated answer
 * - Display unique source documents used in the response
 */
export default function RagChat() {
    /** User-entered question */
    const [question, setQuestion] = useState("");

    /** Answer returned by the RAG system */
    const [answer, setAnswer] = useState("");

    /** List of source documents returned by the backend */
    const [sources, setSources] = useState([]);

    /** Loading state to prevent duplicate submissions */
    const [loading, setLoading] = useState(false);

    /**
     * Sends the user's question to the RAG backend.
     *
     * - Prevents empty submissions
     * - Shows loading state while querying
     * - Updates answer and sources on success
     * - Displays a fallback error message on failure
     */
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

    /**
     * Extracts a clean file name from a source metadata object.
     *
     * Supports different backend key formats and normalizes
     * Windows/Linux paths by returning only the file name.
     */
    function getSourceFileName(src) {
        const sourcePath =
            src.metadata?.source ||
            src.metadata?.file_name ||
            src.metadata?.filename ||
            "";

        return (
            sourcePath
                .split("/")
                .pop()
                .split("\\")
                .pop() || "Unknown file"
        );
    }

    return (
        <div>
            <h3>Chat</h3>

            {/* Question Input */}
            <textarea
                className="input"
                rows={3}
                placeholder="Ask a research question…"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />

            {/* Submit Button */}
            <button
                className="primary-btn"
                onClick={askQuestion}
                disabled={loading}
            >
                {loading ? "Thinking…" : "Ask"}
            </button>

            {/* Answer Section */}
            {answer && (
                <div className="answer-box">
                    <strong>Answer</strong>
                    <p>{answer}</p>
                </div>
            )}

            {/* Sources Section */}
            {sources.length > 0 && (
                <div className="sources-box">
                    <strong>Sources</strong>
                    <ul>
                        {[...new Set(sources.map(getSourceFileName))].map(
                            (fileName, idx) => (
                                <li key={idx}>{fileName}</li>
                            )
                        )}
                    </ul>
                </div>
            )}
        </div>
    );
}
