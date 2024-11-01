import threading
import time
import requests


def read_example() -> None:
    response = requests.get("https://www.example.com")
    print(response.status_code)


sync_start = time.time()
read_example()
read_example()
sync_end = time.time()

print(f"sync: {sync_end - sync_start} seconds")

thread_1 = threading.Thread(target=read_example)
thread_2 = threading.Thread(target=read_example)

thread_start = time.time()

thread_1.start()
thread_2.start()

print("all threads are running...")

thread_1.join()
thread_2.join()

thread_end = time.time()

print(f"threads: {thread_end - thread_start} seconds")
