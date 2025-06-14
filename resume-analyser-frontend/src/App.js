// App.js
import React, { useState, useEffect } from "react";
import './App.css'; // Optional: for your own styles
import Results from './components/results';

function App() {

  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("resume", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("✅ Backend response:", data);
      setResult(data); // passes result to Results
    } catch (error) {
      console.error("❌ Error:", error);
    }
  };

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} accept=".pdf" />
        <button type="submit">Upload Resume</button>
      </form>

      {/* ✅ Conditionally render results */}
      {result && <Results result={result} />}
    </div>
  );
}

export default App;
