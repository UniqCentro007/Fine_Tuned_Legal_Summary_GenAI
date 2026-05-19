import { useState } from "react";
import FileUpload from "./FileUpload.jsx";
import axios from "axios";

function App() {
  const [fileId, setFileId] = useState("");
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUploadComplete = (id) => {
    setFileId(id);
    setSummary("");
    setError("");
  };

  const generateSummary = async () => {
    if (!fileId) {
      setError("Please upload a file before generating a summary.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://localhost:8000/summarize", {
        file_id: fileId,
      });
      setSummary(res.data.summary);
    } catch (err) {
      setError("Unable to generate summary. Check backend availability.");
      console.error("Error generating summary:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "32px auto", padding: "0 16px" }}>
      <h1>Legal Document Summarizer</h1>
      <p>Upload a PDF legal document and generate a concise summary.</p>
      <FileUpload onUploadComplete={handleUploadComplete} />

      {fileId && (
        <div style={{ marginTop: 16 }}>
          <button onClick={generateSummary} disabled={loading}>
            {loading ? "Generating..." : "Generate Summary"}
          </button>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {summary && (
        <div style={{ marginTop: 24 }}>
          <h2>Summary</h2>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f7f7f7", padding: 16, borderRadius: 8 }}>
            {summary}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
