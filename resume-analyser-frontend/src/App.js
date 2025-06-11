// App.js
import React from 'react';
import ResumeUpload from './components/resume_upload';
import './App.css'; // Optional: for your own styles

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Resume Analyzer</h1>
        <p>Get matched with the best tech jobs based on your resume</p>
      </header>

      <main className="app-main">
        <ResumeUpload />
      </main>

      <footer className="app-footer">
        © {new Date().getFullYear()} Resume Analyzer · Built with Flask & React
      </footer>
    </div>
  );
}

export default App;
