import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // Change if backend is deployed elsewhere

function ImageUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");
    try {
      await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("Uploaded!");
      setFile(null);
      if (onUpload) onUpload();
    } catch (err) {
      setStatus("Upload failed.");
    }
  };

  return (
    <div>
      <form onSubmit={handleUpload}>
        <input type="file" accept="image/*" onChange={handleChange} />
        <button type="submit">Upload</button>
      </form>
      {status && <div>{status}</div>}
    </div>
  );
}

export default ImageUpload;