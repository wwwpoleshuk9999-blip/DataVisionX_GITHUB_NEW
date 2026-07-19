class Kernel:
    VERSION = "0.0.1 Genesis"

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print(f"DataVision X {self.VERSION}")
        print("Kernel started.")

    def stop(self):
        self.running = False
        print("Kernel stopped.")
