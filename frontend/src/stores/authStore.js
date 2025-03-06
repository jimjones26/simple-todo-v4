import { writable } from 'svelte/store';

export const auth = writable({
    isAuthenticated: false,
    user: null,
    isLoading: false, // Start with isLoading: false
});

export async function checkAuth() {
    //For a more robust solution in the future, use a dedicated endpoint like /api/auth/status
}
