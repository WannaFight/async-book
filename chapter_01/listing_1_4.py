import multiprocessing
import os


def hello():
    print(f"hello from child proc {os.getpid()}")


if __name__ == "__main__":
    hello_proc = multiprocessing.Process(target=hello)
    hello_proc.start()

    print(f"hello from main proc {os.getpid()}")
    hello_proc.join()
