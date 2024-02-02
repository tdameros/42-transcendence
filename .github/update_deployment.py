import logging
import os

from SSHClient import SSHClient

SSH_HOSTNAME = os.environ.get('SSH_HOSTNAME')
SSH_USERNAME = os.environ.get('SSH_USERNAME')
SSH_PASSWORD = os.environ.get('SSH_PASSWORD')
GITHUB_SERVER_URL = os.environ.get('GITHUB_SERVER_URL')
GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
PROJECT_DIR_NAME = os.environ.get('PROJECT_DIR_NAME')

REPOSITORY_URL = f'{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}'

LOGGER = logging.getLogger('Update Deployment')
LOGGER.setLevel(logging.DEBUG)


def setup_logger(logger: logging.Logger):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def update_project():
    LOGGER.info('Connecting to droplet using ssh...')
    ssh_client = SSHClient()
    if not ssh_client.connect(SSH_HOSTNAME, SSH_USERNAME, SSH_PASSWORD):
        LOGGER.critical('Failed to connect to ssh droplet')
        exit(1)
    LOGGER.info('Update project...')
    status, stdout, stderr = ssh_client.execute_commands([
        f'make -C {PROJECT_DIR_NAME} down',
        f'git -C {PROJECT_DIR_NAME} pull',
        f'make -C {PROJECT_DIR_NAME} up'])
    LOGGER.debug('stdout:\n%s', stdout)
    LOGGER.debug('stderr:\n%s', stderr)
    if not status:
        LOGGER.critical('Failed to execute command')
        exit(1)
    ssh_client.disconnect()


if __name__ == '__main__':
    setup_logger(LOGGER)
    update_project()
    LOGGER.info('Transcendence successfully update!')
