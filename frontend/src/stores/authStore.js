// frontend/src/stores/authStore.js
import { writable } from 'svelte/store';
import { get } from '../utils/api';

export const auth = writable({
    isAuthenticated: false,
    user: null,
    isLoading: true,
});

export async function checkAuth() {
    try {
        const response = await get('/protected');
        // If handleResponse doesn't throw, we have a successful response.
        auth.set({
            isAuthenticated: true,
            user: response, // The response is already the parsed JSON.
            isLoading: false,
        });

    } catch (error) {
        // Any error (network, 401, etc.) will end up here.
        console.error("Error in checkAuth:", error);
        auth.set({
            isAuthenticated: false,
            user: null,
            isLoading: false,
        });
    }
}
