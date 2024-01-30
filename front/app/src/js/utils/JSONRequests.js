
export class JSONRequests {
  static async get(url, headers={}) {
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };
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
    return await JSONRequests.request(`${url}`, options);
  }

  static async request(url, options) {
    const response = await fetch(url, options);
    const body = await response.json();
    return {response: response, body: body};
  }
}
