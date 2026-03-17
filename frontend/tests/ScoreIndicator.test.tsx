import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ScoreIndicator } from '../src/components/ScoreIndicator';

describe('ScoreIndicator', () => {
  it('renders green badge with "Good" label for score >= 80', () => {
    render(<ScoreIndicator score={85} size="large" showLabel />);

    const indicator = screen.getByTestId('score-indicator');
    expect(indicator.textContent).toContain('85');
    expect(indicator.textContent).toContain('Good');

    // Badge should use green color
    const badge = indicator.querySelector('.rounded-full');
    expect(badge?.className).toContain('bg-green-500');
  });

  it('renders yellow badge with "Warning" label for score 50-79', () => {
    render(<ScoreIndicator score={62} showLabel />);

    const indicator = screen.getByTestId('score-indicator');
    expect(indicator.textContent).toContain('62');
    expect(indicator.textContent).toContain('Warning');

    const badge = indicator.querySelector('.rounded-full');
    expect(badge?.className).toContain('bg-yellow-500');
  });

  it('renders red badge with "Poor" label for score < 50', () => {
    render(<ScoreIndicator score={25} showLabel />);

    const indicator = screen.getByTestId('score-indicator');
    expect(indicator.textContent).toContain('25');
    expect(indicator.textContent).toContain('Poor');

    const badge = indicator.querySelector('.rounded-full');
    expect(badge?.className).toContain('bg-red-500');
  });

  it('renders small size by default without label', () => {
    render(<ScoreIndicator score={90} />);

    const indicator = screen.getByTestId('score-indicator');
    expect(indicator.textContent).toContain('90');
    // No label when showLabel is not set
    expect(indicator.textContent).not.toContain('Good');

    const badge = indicator.querySelector('.rounded-full');
    expect(badge?.className).toContain('w-10');
    expect(badge?.className).toContain('h-10');
  });
});
