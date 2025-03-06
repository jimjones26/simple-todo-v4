// frontend/src/utils/api.js

const API_BASE_URL = 'http://127.0.0.1:5000'; // Or your backend URL

async function handleResponse(response) {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

export async function get(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  return handleResponse(response);
}

export async function post(endpoint, data) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: 'include',
  });
  return handleResponse(response);
}
