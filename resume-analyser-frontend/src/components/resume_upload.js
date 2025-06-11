import React, { useState } from 'react';
import axios from 'axios';

const ResumeUpload = ({ setResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("resume", file);

    try {
      setLoading(true);
      const response = await axios.post("http://localhost:5000/upload", formData);
      setResult(response.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Resume (.pdf)</h2>
      <form onSubmit={handleUpload}>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Analyze Resume</button>
      </form>
      {loading && <p>Analyzing...</p>}
    </div>
  );
};

export default ResumeUpload;
