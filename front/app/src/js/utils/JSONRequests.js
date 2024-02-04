
export class JSONRequests {
  static async patch(url, params={}, headers={}) {
    const options = {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };
    const queryString= new URLSearchParams(params).toString();
    url = queryString ? `${url}?${queryString}` : url;
    return await JSONRequests.request(url, options);
  }

  static async delete(url, params={}, headers={}) {
    const options = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };
    const queryString= new URLSearchParams(params).toString();
    url = queryString ? `${url}?${queryString}` : url;
    return await JSONRequests.request(url, options);
  }

  static async get(url, params={}, headers={}) {
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };
    const queryString= new URLSearchParams(params).toString();
    url = queryString ? `${url}?${queryString}` : url;
    return await JSONRequests.request(url, options);
  }

  static async post(url, body, headers={}) {
    const options = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };
    return await JSONRequests.request(url, options);
  }

  static async request(url, options) {
    const response = await fetch(url, options);
    const body = await response.json();
    return {response: response, body: body};
  }
}
