import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ConfidenceBar } from '../src/components/ConfidenceBar';

describe('ConfidenceBar', () => {
  it('renders green bar and percentage for high confidence (>= 0.8)', () => {
    render(<ConfidenceBar score={0.92} />);

    const scoreEl = screen.getByTestId('confidence-score');
    expect(scoreEl.textContent).toBe('92%');

    // The filled bar should use green color class
    const barContainer = screen.getByTestId('confidence-bar');
    const filledBar = barContainer.querySelector('[style]');
    expect(filledBar?.className).toContain('bg-green-500');
    expect(filledBar?.getAttribute('style')).toBe('width: 92%;');
  });

  it('renders yellow bar for medium confidence (0.5 - 0.79)', () => {
    render(<ConfidenceBar score={0.65} />);

    const scoreEl = screen.getByTestId('confidence-score');
    expect(scoreEl.textContent).toBe('65%');

    const barContainer = screen.getByTestId('confidence-bar');
    const filledBar = barContainer.querySelector('[style]');
    expect(filledBar?.className).toContain('bg-yellow-500');
  });

  it('renders red bar for low confidence (< 0.5)', () => {
    render(<ConfidenceBar score={0.3} />);

    const scoreEl = screen.getByTestId('confidence-score');
    expect(scoreEl.textContent).toBe('30%');

    const barContainer = screen.getByTestId('confidence-bar');
    const filledBar = barContainer.querySelector('[style]');
    expect(filledBar?.className).toContain('bg-red-500');
  });

  it('clamps score to 0-1 range', () => {
    render(<ConfidenceBar score={1.5} />);

    const scoreEl = screen.getByTestId('confidence-score');
    expect(scoreEl.textContent).toBe('100%');
  });
});
