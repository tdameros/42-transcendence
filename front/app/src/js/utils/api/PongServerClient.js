import {BaseApiClient} from './BaseClient.js';

export class PongServerClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6006`;

  static URIs = {
    'get-my-game-port': 'game_creator/get_my_game_port/',
  };

  constructor() {
    super();
    this.URL = PongServerClient.URL;
    this.URIs = PongServerClient.URIs;
  }

  async getMyGamePort() {
    const URL = `${this.URL}/${this.URIs['get-my-game-port']}`;
    return await this.getAuthRequest(URL);
  }
}
