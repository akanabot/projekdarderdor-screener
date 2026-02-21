// frontend/src/components/ScoreBadge.jsx
import { CONFIG } from '../config';

export default function ScoreBadge({ score }) {
  let colorClass = "bg-gray-100 text-gray-600"; // WEAK / Default
  
  if (score >= CONFIG.SCORE_STRONG) {
    colorClass = "bg-green-100 text-green-800 border border-green-200";
  } else if (score >= CONFIG.SCORE_MODERATE) {
    colorClass = "bg-yellow-100 text-yellow-800 border border-yellow-200";
  }

  return (
    <span className={`px-2.5 py-1 rounded text-sm font-bold ${colorClass}`}>
      {score}
    </span>
  );
}