import threading
import time


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        if n == 2:
            return 1
        return fib(n - 1) + fib(n - 2)

    print(f"fib ({number}) is {fib(number)}")


def fibs_no_thread():
    print_fib(40)
    print_fib(41)


def fibs_with_thread():
    thread_one = threading.Thread(target=print_fib, args=(40,))
    thread_two = threading.Thread(target=print_fib, args=(41,))

    thread_one.start()
    thread_two.start()

    thread_one.join()
    thread_two.join()


start = time.time()
fibs_no_thread()
end = time.time()
print(f"completed in {end - start:.4f} seconds.")

start = time.time()
fibs_with_thread()
end = time.time()
print(f"threads completed in {end - start:.4f} seconds")
