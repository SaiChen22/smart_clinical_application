interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
  className?: string;
}

const SIZE_CLASSES = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
} as const;

export function LoadingSpinner({ size = 'md', message, className = '' }: LoadingSpinnerProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center py-8 ${className}`}
      data-testid="loading-spinner"
    >
      <div
        className={`${SIZE_CLASSES[size]} animate-spin rounded-full border-4 border-gray-200 border-t-blue-600`}
        role="status"
        aria-label="Loading"
      />
      {message && <p className="mt-3 text-sm text-gray-500">{message}</p>}
    </div>
  );
}
