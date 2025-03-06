// frontend/src/stores/authStore.js
import { writable } from 'svelte/store';
import { get } from '../utils/api'; // Import your API utility

// Initialize the store with a default value (not logged in)
export const auth = writable({
    isAuthenticated: false,
    user: null, // You can store user details here if needed
    isLoading: true, // Add a loading state
});

// Function to check authentication status
export async function checkAuth() {
    try {
        // Make a request to a backend endpoint that requires authentication
        // This endpoint should return user information if logged in, or an error if not.
        const response = await get('/protected'); // Example endpoint - see backend changes below

        if (response) {
            // Update the store with the user data and set isAuthenticated to true
            auth.set({
                isAuthenticated: true,
                user: response, // Assuming the backend returns user data
                isLoading: false,
            });
        } else {
          auth.set({
            isAuthenticated: false,
            user: null,
            isLoading: false,
          });
        }

    } catch (error) {
        // If there's an error (e.g., 401 Unauthorized), the user is not logged in
        auth.set({
            isAuthenticated: false,
            user: null,
            isLoading: false,
        });
    }
}
