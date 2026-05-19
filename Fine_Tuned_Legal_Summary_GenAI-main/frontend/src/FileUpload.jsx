import { useState } from "react";
import axios from "axios";

function FileUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      onUploadComplete(res.data.file_id);
    } catch (err) {
      setError("Upload failed. Check backend availability.");
      console.error("Upload failed:", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      <label>
        Choose a PDF file:
        <input type="file" accept=".pdf" onChange={handleFileChange} />
      </label>
      <div style={{ marginTop: 10 }}>
        <button onClick={handleUpload} disabled={uploading}>
          {uploading ? "Uploading..." : "Upload File"}
        </button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default FileUpload;
