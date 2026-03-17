interface ConfidenceBarProps {
  score: number;
}

export function ConfidenceBar({ score }: ConfidenceBarProps) {
  // Clamp score between 0 and 1
  const clampedScore = Math.max(0, Math.min(1, score));
  const percentage = Math.round(clampedScore * 100);

  // Determine color based on score
  let colorClass = 'bg-red-500';
  let textColorClass = 'text-red-700';
  
  if (clampedScore >= 0.8) {
    colorClass = 'bg-green-500';
    textColorClass = 'text-green-700';
  } else if (clampedScore >= 0.5) {
    colorClass = 'bg-yellow-500';
    textColorClass = 'text-yellow-700';
  }

  return (
    <div className="w-full" data-testid="confidence-bar">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">Confidence Score</span>
        <span className={`text-sm font-medium ${textColorClass}`} data-testid="confidence-score">
          {percentage}%
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full ${colorClass} transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}
