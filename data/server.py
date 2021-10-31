

import time
import shyft.time_series as sts
from pathlib import Path


def start_dtss(root_dir: Path):
    s = sts.DtsServer()
    s.set_container(f"frost", str(root_dir))
    s.set_listening_port(20001)
    s.start_async()
    return s


if __name__ == "__main__":
    root_dir = Path("dtss")

    s = start_dtss(root_dir=root_dir)
    while True:
        print(s.alive_connections)
        time.sleep(1)
