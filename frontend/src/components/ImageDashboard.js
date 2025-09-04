import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function ImageDashboard() {
  const [files, setFiles] = useState([]);

  const fetchFiles = async () => {
    const res = await axios.get(`${API_URL}/files`);
    setFiles(res.data.reverse()); // Show newest first
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div>
      <h2>Uploaded Images</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {files.map((file) => (
          <div key={file.id} style={{ border: "1px solid #eee", padding: "10px" }}>
            <img
              src={`${API_URL}/uploads/${file.filename}`}
              alt={file.filename}
              style={{ width: 150, height: 100, objectFit: "cover" }}
            />
            <div><b>{file.filename}</b></div>
            <div>{new Date(file.upload_time).toLocaleString()}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ImageDashboard;
