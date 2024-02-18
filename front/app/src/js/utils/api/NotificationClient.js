import {BaseApiClient} from './BaseClient.js';

export class NotificationClient extends BaseApiClient {
  static URL = `https://${window.location.hostname}:6005`;

  static URIs = {
    'delete-notification': 'notification/user/:notification_id/',
  };

  constructor() {
    super();
    this.URL = NotificationClient.URL;
    this.URIs = NotificationClient.URIs;
  }

  async deleteNotification(notificationId) {
    const URI = this.URIs['delete-notification'].replace(
        ':notification_id', notificationId,
    );
    const URL = `${this.URL}/${URI}`;
    return await this.deleteAuthRequest(URL);
  }
}
