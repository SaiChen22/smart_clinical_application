import type { DataQualityResponse, QualityBreakdown } from '../../types';
import { ScoreIndicator } from '../../components/ScoreIndicator';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { ErrorMessage } from '../../components/ErrorMessage';

interface DataQualityPanelProps {
  result: DataQualityResponse | null;
  loading?: boolean;
  error?: string | null;
}

const DIMENSIONS: { key: keyof QualityBreakdown; label: string }[] = [
  { key: 'completeness', label: 'Completeness' },
  { key: 'accuracy', label: 'Accuracy' },
  { key: 'timeliness', label: 'Timeliness' },
  { key: 'clinical_plausibility', label: 'Clinical Plausibility' },
];

export function DataQualityPanel({ result, loading = false, error = null }: DataQualityPanelProps) {
  if (error) {
    return <ErrorMessage message={error} />;
  }
  if (loading) {
    return <LoadingSpinner message="Analyzing data quality..." />;
  }

  if (!result) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200 p-12">
        <div className="text-center">
          <p>Submit patient data to see quality analysis</p>
        </div>
      </div>
    );
  }

  const getBarColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="space-y-6" data-testid="data-quality-result">
      {/* Overall Score */}
      <div className="bg-white p-6 rounded-lg shadow-md flex flex-col items-center justify-center">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Overall Data Quality</h3>
        <div data-testid="overall-score">
          <ScoreIndicator score={result.overall_score} size="large" showLabel />
        </div>
      </div>

      {/* Dimensional Breakdown */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quality Dimensions</h3>
        <div className="space-y-4">
          {DIMENSIONS.map((dim) => {
            const score = result.breakdown[dim.key];
            return (
              <div key={dim.key}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">{dim.label}</span>
                  <span className="text-sm font-medium text-gray-900">{Math.round(score)}/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className={`h-2.5 rounded-full ${getBarColor(score)} transition-all duration-500`}
                    style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Issues Detected */}
      {result.issues_detected.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md" data-testid="issues-list">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Issues Detected</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Field
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Issue
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Severity
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {result.issues_detected.map((issue, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {issue.field}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {issue.issue}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full border ${getSeverityBadge(issue.severity)}`}>
                        {issue.severity.toUpperCase()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
