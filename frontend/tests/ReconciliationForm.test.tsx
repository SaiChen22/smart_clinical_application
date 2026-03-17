import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ReconciliationForm } from '../src/features/reconciliation/ReconciliationForm';

describe('ReconciliationForm', () => {
  it('calls onSubmit with form data when submitted', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);

    render(<ReconciliationForm onSubmit={onSubmit} />);

    const submitButton = screen.getByTestId('reconciliation-submit');
    fireEvent.click(submitButton);

    expect(onSubmit).toHaveBeenCalledTimes(1);
    // Should be called with the default initial state
    const callArg = onSubmit.mock.calls[0][0];
    expect(callArg.patient_context.age).toBe(58);
    expect(callArg.patient_context.conditions).toContain('type 2 diabetes');
    expect(callArg.sources).toHaveLength(2);
    expect(callArg.sources[0].system).toBe('Hospital EHR');
    expect(callArg.sources[0].medication).toBe('Metformin 500mg');
    expect(callArg.sources[1].system).toBe('Pharmacy');
    expect(callArg.sources[1].medication).toBe('Metformin 1000mg');
  });

  it('shows loading state and disables submit button', () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);

    render(<ReconciliationForm onSubmit={onSubmit} loading />);

    const submitButton = screen.getByTestId('reconciliation-submit');
    expect(submitButton).toBeDisabled();
    expect(submitButton.textContent).toBe('Reconciling...');
  });

  it('displays error message when error prop is provided', () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);

    render(<ReconciliationForm onSubmit={onSubmit} error="API Error (503): LLM timeout" />);

    const alert = screen.getByRole('alert');
    expect(alert.textContent).toContain('API Error (503): LLM timeout');
  });
});
