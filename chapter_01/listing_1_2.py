import os
import threading

print(f"Python proc: {os.getpid()}")

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f"{total_threads} thread(s)")
print(f"current: {thread_name}")
