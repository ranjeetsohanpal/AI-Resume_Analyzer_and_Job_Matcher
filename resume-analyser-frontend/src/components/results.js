import React from 'react';

function Results({ result }) {
  if (!result) return null;

  const { name, skills, summary, matched_jobs } = result;

  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold">Hi, {name || 'Candidate'}</h3>

      <p className="mt-2">
        <strong>Summary:</strong>{' '}
        {summary ? summary : 'No summary extracted'}
      </p>

      <p className="mt-2">
        <strong>Skills:</strong>{' '}
        {Array.isArray(skills) && skills.length > 0 ? skills.join(', ') : 'Not detected'}
      </p>

      <h4 className="mt-4 font-semibold">Top Job Matches:</h4>
      <ul className="list-disc pl-5">
        {Array.isArray(matched_jobs) && matched_jobs.length > 0 ? (
          matched_jobs.map((job, idx) => (
            <li key={idx} className="mb-2">
              <strong>{job.title || 'Job Title N/A'}</strong> – Match Score: {job.score ?? 'N/A'}%
              <br />
              <span>
                Missing Skills:{' '}
                {Array.isArray(job.missing_skills) && job.missing_skills.length > 0
                  ? job.missing_skills.join(', ')
                  : 'None'}
              </span>
            </li>
          ))
        ) : (
          <li>No matching jobs found.</li>
        )}
      </ul>
    </div>
  );
}

export default Results;
