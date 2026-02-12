# %%  normal sequential 
import string
import time
from functools import wraps
def evaluate_execution_time1(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        t_start = time.perf_counter()
        results = fn(*args, **kwargs)
        t_end = time.perf_counter()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] \033[4;32mcompleted in {t_end - t_start:.4f}s\033[0m")
        print()
        return results
    return wrapper

    
def fetch_data1(param):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data Streaming Started with request: {param}\n")
    time.sleep(param)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Done with {param}\n")
    return param

@evaluate_execution_time1
def main1():
    li = [1,2]
    results = []
    for i in li:
        result = fetch_data1(li[i-1])
        results.append(result)
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fectching data {i} fully completed\n")
    return results



# %%  asyncio 
import asyncio,time
from functools import wraps
def evaluate_execution_time(fn):
    @wraps(fn)
    async def wrapper(*args,**kwargs):
        t_start = time.perf_counter()
        results = await fn(*args, **kwargs)
        t_end = time.perf_counter()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] \033[4;32mcompleted in {t_end - t_start:.4f}s\033[0m")
        print()
        return results
    return wrapper

    
async def fetch_data(param):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data Streaming Started with request: {param}\n")
    await asyncio.sleep((param))
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Done with {param}\n")
    return param

@evaluate_execution_time
async def main():
            li = [1, 2]
            results = await asyncio.gather(*(fetch_data(x) for x in li))
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fectching data fully completed\n")
            return results

if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'sequential'
    if mode.lower() == 'async':
        print(f"\n \033[32m {mode=}\n \033[0m")
        results = asyncio.run(main())
        print(results)
    else:
        print(f"\033[ 32m {mode=}")
        results = main1()
        print(results)



# %% asyncio example 2 
import random
import asyncio 

async def fetch_something(x):
            name = random.choice(["Alice", "Bob", "Carlos", "Dina", "Evan"])
            print(f"receiving data from {name} (task {x}) ... ")
            await asyncio.sleep(1)
            return name
    
async def monitor_something(y):
            print(f"detected {y} is working")
            return y

async def main():
    while True:
        tasks = [fetch_something(i) for i in range(1,6)]
        results = await asyncio.gather(*tasks)
        await monitor_something(results)
        print(results)
          
await main()
    
    



# %%  pyper

from pyper import task 
import asyncio
import random
import string

async def say_hi(name):
    '''simulating monitoring function -> detected new customer registered'''
    return print(f"Hi {name}!")

async def select_a_customer():
    '''simulating data streaming -> customer registered'''
    length = random.randint(4, 8)
    return ''.join(random.choice(string.ascii_lowercase)
                   for _ in range(length)).capitalize()
    
async def main():
    while True:
     name = await select_a_customer()
     await say_hi(name)
     await asyncio.sleep(1)
 
await main()

# %%
