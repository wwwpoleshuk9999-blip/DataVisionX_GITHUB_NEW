import time


class HealthMonitor:
    def __init__(self):
        self.start_time = None
        self.status = "STOPPED"

    def start(self):
        self.start_time = time.time()
        self.status = "RUNNING"

    def stop(self):
        self.status = "STOPPED"

    def report(self):
        uptime = 0

        if self.start_time:
            uptime = int(time.time() - self.start_time)

        return {
            "status": self.status,
            "uptime": uptime
        }


health = HealthMonitor()
