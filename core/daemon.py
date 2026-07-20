import signal
import time

from core.kernel import Kernel


kernel = Kernel()


def shutdown(signum, frame):
    kernel.stop()
    raise SystemExit(0)


def run():
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    kernel.start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    run()
