from django.test import TestCase
from django.urls import reverse

from api.models import Notification
from api import error_message as error
from notification import settings


class PostUserNotificationTest(TestCase):
    def post_user_notification(self, data):
        url = reverse('user-notification')

        response = self.client.post(url, data, content_type='application/json')
        body = response.json()

        return response, body

    def test_send_friend_request(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
            'user_list': [1],
            'data': '4',
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(body, {'message': 'Notification created'})

        notifications = Notification.objects.all()
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications[0].title, data['title'])
        self.assertEqual(notifications[0].type, data['type'])
        self.assertEqual(notifications[0].owner_id, data['user_list'][0])
        self.assertEqual(notifications[0].data, data['data'])

    def test_send_tournament_start(self):
        data = {
            'title': 'Tournament `Born2Smash` started',
            'type': 'tournament_start',
            'user_list': [1, 2, 3],
            'data': '1',
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(body, {'message': 'Notification created'})

        notifications = Notification.objects.all()
        self.assertEqual(notifications.count(), 3)
        self.assertEqual(notifications[0].title, data['title'])
        self.assertEqual(notifications[0].type, data['type'])
        self.assertEqual(notifications[0].owner_id, data['user_list'][0])
        self.assertEqual(notifications[0].data, data['data'])
        self.assertEqual(notifications[1].title, data['title'])
        self.assertEqual(notifications[1].type, data['type'])
        self.assertEqual(notifications[1].owner_id, data['user_list'][1])
        self.assertEqual(notifications[1].data, data['data'])
        self.assertEqual(notifications[2].title, data['title'])
        self.assertEqual(notifications[2].type, data['type'])
        self.assertEqual(notifications[2].owner_id, data['user_list'][2])
        self.assertEqual(notifications[2].data, data['data'])

    def test_invalid_title(self):
        data = {
            'title': None,
            'type': 'friend_request',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.MISSING_TITLE]})

    def test_invalid_body(self):
        data = "invalid body"

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.BAD_JSON_FORMAT]})

    def test_title_int(self):
        data = {
            'title': 1,
            'type': 'friend_request',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_TITLE_FORMAT]})

    def test_title_empty(self):
        data = {
            'title': '',
            'type': 'friend_request',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_TITLE_LENGTH]})

    def test_title_too_long(self):
        data = {
            'title': 'a' * (settings.TITLE_MAX_LENGTH + 1),
            'type': 'friend_request',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_TITLE_LENGTH]})

    def test_missing_type(self):
        data = {
            'title': 'Friend request from John Doe',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.MISSING_TYPE]})

    def test_invalid_type(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 1,
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_TYPE_FORMAT]})

    def test_type_not_exist(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'invalid_type',
            'user_list': [1],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.TYPE_NOT_EXIST]})

    def test_missing_user_list(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.MISSING_USER_LIST]})

    def test_invalid_user_list(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
            'user_list': 1,
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_USER_LIST_FORMAT]})

    def test_user_list_str(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
            'user_list': [1, 2, 3, '1', 5],
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_USER_LIST_FORMAT]})
        notifications = Notification.objects.all()
        self.assertEqual(notifications.count(), 0)

    def test_invalid_data(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
            'user_list': [1],
            'data': 1,
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_DATA_FORMAT]})

    def test_data_dict(self):
        data = {
            'title': 'Friend request from John Doe',
            'type': 'friend_request',
            'user_list': [1],
            'data': {'key': 'value'},
        }

        response, body = self.post_user_notification(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body, {'errors': [error.INVALID_DATA_FORMAT]})
        notifications = Notification.objects.all()
        self.assertEqual(notifications.count(), 0)
