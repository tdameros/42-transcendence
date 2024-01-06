import time

import paramiko


class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, hostname: str, username: str,
                password: str, port: int = 22, timeout: int = 120,
                wait: int = 5) -> bool:
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while elapsed_time < timeout:
            try:
                self.client.connect(hostname, port, username, password)
                return True
            except Exception:
                time.sleep(wait)
                elapsed_time = time.time() - start_time
        return False

    def disconnect(self):
        self.client.close()

    def execute_command(self, command: str):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return True, stdout.read().decode(), stderr.read().decode()
        except Exception:
            return False, None, None

    def execute_commands(self, commands: list[str]):
        return self.execute_command(' && '.join(commands))
