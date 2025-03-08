// frontend/src/utils/api.js

const API_BASE_URL = 'http://127.0.0.1:5001'; // Or your backend URL

async function handleResponse(response) {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

export async function get(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function post(endpoint, data) {
  const method = data?._method || 'POST'; // Use _method to override
  delete data?._method; // Remove _method from the body

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: 'include',
  });
  return handleResponse(response);
}

export async function patch(endpoint, data) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: 'include',
  });
  return handleResponse(response);
}

// Add a logout function
export async function logout() {
    return get('/logout');
}
