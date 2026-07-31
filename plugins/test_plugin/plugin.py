class Plugin:

    id = "test_plugin"
    name = "Test Plugin"
    version = "1.0.0"
    description = "Phoenix test plugin"

    def start(self):
        print("Test Plugin started")

    def stop(self):
        print("Test Plugin stopped")
