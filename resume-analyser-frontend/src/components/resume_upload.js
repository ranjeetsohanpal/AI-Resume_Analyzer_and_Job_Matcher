import React, { useState } from 'react';
import Results from './results';

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      console.log("✅ Response from backend:", data);
      setResult(data);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-2">Upload Your Resume (PDF)</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
        <button type="submit" className="ml-2 bg-blue-500 text-white px-4 py-1 rounded">
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      <Results result={result} />
    </div>
  );
}

export default ResumeUpload;
