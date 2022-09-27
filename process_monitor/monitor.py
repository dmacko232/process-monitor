from typing import List, Tuple
import time
import platform
import os
import resource
import subprocess

def monitor_process_psutil(executable_path: str, second_interval: int) -> List[Tuple[float, int, int]]:
    """Monitor process each interval while its running"""
    
    import psutil

    data = []
    try:
        with psutil.Popen(executable_path) as proc:
            proc.cpu_percent() # first blank call to set it

            while proc.poll() is None:
                proc_mem = proc.memory_info().rss
                proc_cpu = proc.cpu_percent() / psutil.cpu_count()
                open_files = 0
                if platform.system() == "Windows":
                    open_files = proc.num_handles()
                else:
                    open_files = proc.num_fds()
                data.append((proc_cpu, proc_mem, open_files))
                time.sleep(second_interval)
    except Exception as e:
        print(e)
    return data

def monitor_process_standard(executable_path: str, second_interval: int) -> List[Tuple[float, int, int]]:
    
    data = []
    start_time = time.time()
    elapsed_cpu_time = 0
    try:
        with subprocess.Popen(executable_path) as proc:
            while proc.poll() is None:
                usage = resource.getrusage(resource.RUSAGE_CHILDREN)

                # cpu
                end_time = time.time()
                cpu_time = usage.ru_utime + usage.ru_stime
                proc_cpu = (cpu_time - elapsed_cpu_time) / (end_time - start_time) * 100
                elapsed_cpu_time += cpu_time
                start_time = end_time

                # mem
                proc_mem = usage.ru_maxrss # memory size

                # files
                open_files = 0
                if platform.system() == "Windows":
                    open_files = 0 # TODO
                    # https://github.com/giampaolo/psutil/blob/master/psutil/_psutil_windows.c
                    # we could copy code from here but whats the point when not using psutil?
                    # I just hate Windows, why this cant be easy?
                    # We could also leverage https://learn.microsoft.com/en-us/sysinternals/downloads/handle
                    # but that doesnt have to be always installed afaik
                    print("Warning: counting file handles for Windows not implemented. By default 0")
                else:
                    open_files = len(os.listdir(os.path.join("/proc", str(proc.pid), "fd")))
                data.append((proc_cpu, proc_mem, open_files))
                time.sleep(second_interval)
    except Exception as e:
        print(e)
    return data
