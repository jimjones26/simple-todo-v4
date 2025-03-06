import { writable } from 'svelte/store';
import { get } from '../utils/api';

export const auth = writable({
    isAuthenticated: false,
    user: null,
    isLoading: true // Start with loading state
});

export async function checkAuth() {
    auth.update(current => ({ ...current, isLoading: true }));
    try {
        const response = await get('/auth/status');
        auth.set({ isAuthenticated: true, user: response, isLoading: false });
    } catch (error) {
        auth.set({ isAuthenticated: false, user: null, isLoading: false });
    }
}