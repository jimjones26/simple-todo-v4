import { render, screen } from '@testing-library/svelte';
import TeamTasks from '../components/TeamTasks.svelte';
import { vi, describe, it, expect } from 'vitest';

describe('TeamTasks Component', () => {
  it('renders without errors', () => {
    // Mock props (teamId is required)
    const teamId = 123;

    // Render the component
    render(TeamTasks, { props: { teamId } });

    // Check for some static content (e.g., a heading)
    expect(screen.getByText('Team Tasks')).toBeInTheDocument();
  });
});
