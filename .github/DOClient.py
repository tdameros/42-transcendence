from time import sleep

from pydo import Client


class DOClient:

    def __init__(self, api_key):
        self.client = Client(token=api_key)

    def restore_droplet_and_wait(self, droplet_id: str,
                                 image_id: str) -> str:
        response = self.restore_droplet(droplet_id, image_id)
        action_id = response.get('action').get('id')
        status = self.get_droplet_action_status(droplet_id,
                                                action_id)
        while status == "in-progress":
            sleep(5)
            status = self.get_droplet_action_status(droplet_id,
                                                    action_id)
        return status

    def restore_droplet(self, droplet_id: str, image_id: str) -> dict:
        request = {
            "type": "restore",
            "image": image_id,
        }
        return self.client.droplet_actions.post(droplet_id=droplet_id,
                                                body=request)

    def get_droplet_action_status(self, droplet_id: str,
                                  action_id: str) -> str:
        response = self.client.droplet_actions.get(droplet_id=droplet_id,
                                                   action_id=action_id)
        return response.get('action').get('status')
