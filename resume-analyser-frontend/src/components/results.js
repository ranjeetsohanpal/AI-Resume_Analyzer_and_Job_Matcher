import React from 'react';

const Results = ({ result }) => {
  if (!result) return null;

  return (
    <div className="results-container">
      <h3>Hello, {result.name}</h3>
      <h4>Extracted Skills:</h4>
      <ul>{result.skills.map(skill => <li key={skill}>{skill}</li>)}</ul>

      <h4>Matching Jobs:</h4>
      {result.matched_jobs.map((job, idx) => (
        <div key={idx}>
          <strong>{job.title}</strong>
          <p>Match: {job.score}%</p>
          <p>Missing Skills: {job.missing_skills.join(", ")}</p>
        </div>
      ))}
    </div>
  );
};

export default Results;
