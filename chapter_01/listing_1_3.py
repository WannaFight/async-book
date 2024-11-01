import threading


def hello():
    print(f"Hello from thread {threading.current_thread()}")


hello_thread = threading.Thread(target=hello)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f"{total_threads} thread(s)")
print(f"current: {thread_name}")

hello_thread.join()
