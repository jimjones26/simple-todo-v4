// @ts-ignore
import { expect, test, beforeEach, vi, describe, MockedFunction } from 'vitest';
import { get, post } from './api.js';

beforeEach(() => {
  // Reset fetch mock before each test
  global.fetch = vi.fn();
});

describe('get function', () => {
  test('makes a GET request and returns JSON data on success', async () => {
    // Arrange: Mock a successful response
    const mockData = {  data: 'test data' };
    // @ts-ignore
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockData),
    });

    // Act: Call the get function
    const result = await get('/test');

    // Assert: Verify the request and response
    expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:5001/test', {credentials: 'include'});
    expect(result).toEqual(mockData);
  });

  test('throws an error on HTTP error status', async () => {
    // Arrange: Mock an error response
    // @ts-ignore
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    // Act & Assert: Expect the function to throw
    await expect(get('/test')).rejects.toThrow('HTTP error! status: 404');
  });

  test('throws an error if fetch fails', async () => {
    // Arrange: Mock a network error
    const error = new Error('Network error');
    // @ts-ignore
    global.fetch.mockRejectedValueOnce(error);

    // Act & Assert: Expect the function to propagate the error
    await expect(get('/test')).rejects.toThrow('Network error');
  });
});

describe('post function', () => {
  test('makes a POST request with data and returns JSON on success', async () => {
    // Arrange: Mock a successful response
    const postData = { key: 'value' };
    const mockResponse = { result: 'success' };
    // @ts-ignore
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockResponse),
    });

    // Act: Call the post function
    const result = await post('/test', postData);

    // Assert: Verify the request details and response
    expect(global.fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:5001/test',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postData),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  test('throws an error on HTTP error status', async () => {
    // Arrange: Mock an error response
    // @ts-ignore
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    // Act & Assert: Expect the function to throw
    await expect(post('/test', {})).rejects.toThrow('HTTP error! status: 500');
  });

  test('throws an error if fetch fails', async () => {
    // Arrange: Mock a network error
    const error = new Error('Network error');
    // @ts-ignore
    global.fetch.mockRejectedValueOnce(error);

    // Act & Assert: Expect the function to propagate the error
    await expect(post('/test', {})).rejects.toThrow('Network error');
  });
});