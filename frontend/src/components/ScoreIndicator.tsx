interface ScoreIndicatorProps {
  score: number;
  size?: 'small' | 'large';
  showLabel?: boolean;
}

export function ScoreIndicator({ score, size = 'small', showLabel = false }: ScoreIndicatorProps) {
  let bgColorClass = 'bg-red-500';
  let textColorClass = 'text-red-700';

  if (score >= 80) {
    bgColorClass = 'bg-green-500';
    textColorClass = 'text-green-700';
  } else if (score >= 50) {
    bgColorClass = 'bg-yellow-500';
    textColorClass = 'text-yellow-700';
  }

  const sizeClasses = size === 'large' ? 'w-24 h-24 text-3xl' : 'w-10 h-10 text-sm';
  const label = showLabel ? (score >= 80 ? 'Good' : score >= 50 ? 'Warning' : 'Poor') : null;

  return (
    <div className="flex flex-col items-center" data-testid="score-indicator">
      <div 
        className={`flex items-center justify-center rounded-full text-white font-bold shadow-md ${sizeClasses} ${bgColorClass}`}
      >
        {Math.round(score)}
      </div>
      {label && <span className={`mt-2 font-semibold ${textColorClass}`}>{label}</span>}
    </div>
  );
}
