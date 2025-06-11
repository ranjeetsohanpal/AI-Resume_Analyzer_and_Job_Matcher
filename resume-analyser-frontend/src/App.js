import React, { useState } from 'react';
import ResumeUpload from './components/resume_upload';
import Results from './components/results';

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <div>
      <h1>AI Resume Analyzer and Job Matcher </h1>
      <ResumeUpload setResult={setResult} />
      <Results result={result} />
      </div>
    </div>
  );
}

export default App;

