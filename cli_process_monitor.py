import subprocess
import argparse

import os
import sys

from process_monitor.io import save_json
from process_monitor.monitor import monitor_process_psutil, monitor_process_standard

def main() -> None:

    parser = argparse.ArgumentParser(
        description="Execute process and monitor it's cpu usage, memory usage, and open files.")
    parser.add_argument(
        "executable_path",
        type=str, 
        help="path to file to execute as process and monitor"
    )
    parser.add_argument(
        "output_path",
        type=str, 
        help="path to where store output in json"
    )
    parser.add_argument(
        "second_interval",
        type=int, 
        help="second interval in which we wish to sync"
    )
    parser.add_argument(
        "--use_psutil",
        help="whether to use non-standard pustil library",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    if not os.path.exists(args.executable_path):
        print("Executable path doesn't exist! Exiting.")
        sys.exit(1)
    if args.use_psutil:
        data = monitor_process_psutil(args.executable_path, args.second_interval)
    else:
        data = monitor_process_standard(args.executable_path, args.second_interval)
    save_json(data, args.output_path)

if __name__ == "__main__":
    main()
