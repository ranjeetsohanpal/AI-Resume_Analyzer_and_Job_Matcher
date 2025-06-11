import React from 'react';

function Results({ result }) {
  if (!result) return null;

  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold">Hi, {result.name}</h3>
      <p><strong>Skills:</strong> {result.skills.join(', ')}</p>

      <h4 className="mt-2 font-semibold">Top Job Matches:</h4>
      <ul className="list-disc pl-5">
        {result.matched_jobs.map((job, idx) => (
          <li key={idx} className="mb-2">
            <strong>{job.title}</strong> - Match Score: {job.score}%<br />
            <span>Missing Skills: {job.missing_skills.length > 0 ? job.missing_skills.join(', ') : 'None'}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Results;
