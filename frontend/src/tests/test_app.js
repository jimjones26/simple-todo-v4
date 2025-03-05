import { render, screen } from '@testing-library/svelte';
import App from './App.svelte';
import { describe } from 'vitest';

describe('App', () => {
  test('mounts correctly', () => {
    // Render the App component
    render(App);

    // Check for an element that should be present when mounted
    const { container } = render(App);
    expect(container).toBeInTheDocument();
  });
});