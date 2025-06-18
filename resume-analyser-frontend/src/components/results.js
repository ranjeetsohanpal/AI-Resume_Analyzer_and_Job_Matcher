import React from 'react';

function Results({ result }) {
  if (!result) return null;

  const {
    name,
    skills,
    summary,
    matched_job_titles,
    sim_scores,
    req_skills,
    missing_skills
  } = result;

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
        {Array.isArray(matched_job_titles) && matched_job_titles.length > 0 ? (
          matched_job_titles.map((title, idx) => (
            <li key={idx} className="mb-4">
              <p><strong>Job Title:</strong> {title}</p>
              <p><strong>Match Score:</strong> {sim_scores[idx]}%</p>
              <p>
                <strong>Required Skills:</strong>{' '}
                {Array.isArray(req_skills[idx]) && req_skills[idx].length > 0
                  ? req_skills[idx].join(', ')
                  : 'N/A'}
              </p>
              <p>
                <strong>Missing Skills:</strong>{' '}
                {Array.isArray(missing_skills[idx]) && missing_skills[idx].length > 0
                  ? missing_skills[idx].join(', ')
                  : 'None'}
              </p>
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
