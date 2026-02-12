# %% example of coroutine: a way to pause/resume work cooperatively within a single thread

import datetime
def date_coroutine(_date:datetime.datetime):
        
    '''
    This function demonstrates that a coroutine pauses execution at `yield`
    and resumes when a value is sent via `.send(value)`.

    In a generator/coroutine, `yield` does two things:
    1. Pauses execution and hands control back to the caller.
    2. Receives a value when the caller resumes it with `.send(value)`.
    '''

    print(f"Your appointmnet is scheduled for {_date.strftime('%Y/%m/%d, %H:%M')}")
    while True:
        current_date = (yield)
        if current_date > _date:
            print("Oops, your appointment already passed")
        else:
            print("You have time")

d1 = datetime.datetime(1981, 6, 29, 1, 0)
print('run line 13')
coroutine = date_coroutine(d1)
print('run line 15')
coroutine.__next__()  # runs the function up to the line with (yield)
print('run line 17')
d2 = datetime.datetime(1918,5,3)
print('run line 19')
coroutine.send(d2)
print('run line 21')

# %% example of multithreading: within a process, multiple threads overlap I/O waits

'''
Example of multithreading in a single process to overlap I/O waits.
While one worker sleeps (simulated I/O), others can run.

This is concurrency, not true CPU parallelism in CPython (due to the GIL).

In this example, sequential execution would take ~10 seconds (0+1+2+3+4).
Because the sleeps overlap, total time is ~4 seconds (the longest sleep).


This is a “from first principles” example. 
In production we usually use standard library abstractions 
(ThreadPoolExecutor, Queue, etc.) instead of managing raw Thread objects ourselves.
'''

import time
import threading

def worker(num, callback):
    print(f"worker {num} starting ...")
    time.sleep(num) # simulate somework
    print(f"worker {num} finished.")
    callback(num) # call the call back

def callback_function(num):
    print(f"callback for worker {num} called.")

if __name__ == "__main__":
    '''
    if __name__ == "__main__": prevents the code from running on import. 
    Its essential for multiprocessing (especially on Windows, to avoid recursive process spawning), 
    and its good practice for threading too, 
    but threads dont require it the same way processes do.
    '''
    start_time = time.time()
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i, callback_function))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        print(thread)
        # wait for this thread to finish, when the loop finishes it guarantees
        # every thread has finished.
        thread.join()
    
    end_time = time.time()
    print(f"finished in {end_time - start_time}s")
