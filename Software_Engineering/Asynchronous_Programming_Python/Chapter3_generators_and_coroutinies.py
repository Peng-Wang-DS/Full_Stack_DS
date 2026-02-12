# %% 
import numpy as np
li1 = iter(range(1000000000))
li1.__next__()


li2 = (x for x in range(1000000000))
type(li2)

import sys
print(sys.getsizeof(li1),
sys.getsizeof(li2))



# %% 
import numpy as np

def sin_temp(mean=15, std=5):
    print("1")
    rng = np.random.default_rng()
    print("2")

    temps = [rng.normal(mean, std) for _ in range(365)]
    print("3")

    yield min(temps), max(temps)
    print("4")
    threshold = yield
    print("5")

    days_over_threshold = len([t for t in temps if t > threshold])
    print("6")

    yield days_over_threshold


gen = sin_temp()

# it will reach until yield min(temps), max(temps), after run this line, pause
print(next(gen))

# send(None) advances the generator to the threshold = yield line so that
# it is ready to receive a real value later via send(value).
gen.send(None)


print(gen.send(18))

print(type(gen))




# %% 
import numpy as np
def sim_temp(mean: float = 15, stdv: float = 5):
    try:
        rng = np.random.default_rng()
        print('line 1')
        temps = [rng.normal(mean, stdv) for _ in range(365)]
        print('line 2')
        yield min(temps), max(temps)
        print('line 3')
        threshold = (yield)
        print('line 4')
        print(f'Threshold: {threshold}')
        days_over_threshold = len([d for d in temps if d > threshold])
        print('line 5')
        print(f'There were:{days_over_threshold} days over {threshold} degrees')
        yield days_over_threshold
        print('line 6')
    except GeneratorExit:
        print('This is already closed')
        return 0


try:
    m = 22
    std = 8
    s = sim_temp(m, std)
    print(f'Simulating the temp around {m} with standard deviation of {std}')
    min, max = s.__next__()
    s.close()
    print(f'The temp moves between {min} and {max} centigrades')
    s.__next__()
    s.send((max - min) / 2)
except StopIteration:
    print('Nothing else in the coroutine')



# %% 

import time

def pi_approximation(terms):
    denominator = 1.0
    sign = 1.0
    result = 0.0

    for _ in range(terms):
        result += sign * (4.0 / denominator)
        sign *= -1
        denominator += 2

    return result

def pi_approximation_generator(terms):
    denominator = 1.0
    sign = 1.0
    result = 0.0

    for _ in range(terms):
        result += sign * (4.0 / denominator)
        sign *= -1
        denominator += 2
        yield result

if __name__ == '__main__':
    num_iters = 1000000        
    for i in range(3):
        start = time.process_time_ns()
        pi_approx = pi_approximation(num_iters)
        end = time.process_time_ns()
        print(f'PI: {pi_approx} took {(end - start)/1000000000} seconds')
        start = time.process_time_ns()
        for approx in pi_approximation_generator(num_iters):
            pi_approx = approx
        end = time.process_time_ns()
        print(f'PI using generator: {pi_approx} {(end - start)/1000000000} seconds')


start = time.process_time_ns()
sum((i**0.5) * (i**0.25) for i in range(1, 10_000_000))
time.sleep(2)
end = time.process_time_ns()
(end - start) / 100000000



# %%
import json
import asyncio
import requests
import time
from sseclient import SSEClient


session = requests.Session()
session.headers.update(
    {"User-Agent": "AsynchronousProgrammingExamples/1.0 (contact: example@example.com)"}
)
messages = SSEClient(
    "https://stream.wikimedia.org/v2/stream/recentchange", session=session
)
batch_size = 3
vals = []

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

async def sse_client_get_values():
    log("sse_client_get_values: start")
    batch = []
    for event in messages:
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                if change['meta']['domain'] == 'canary' or change['bot'] == True:
                    continue            
                if len(batch) < batch_size:
                    batch.append(change['user'])
                else: 
                    log("sse_client_get_values: returning batch")
                    return batch                

async def fetcher():
    log("fetcher: start")
    while True:
        io_vals = await sse_client_get_values()
        log(f"fetcher: got {len(io_vals)} users")
        vals.extend(io_vals)
        await asyncio.sleep(1)

async def monitor():
    log("monitor: start")
    while True:
        log(f"monitor: vals size {len(vals)}")
        await asyncio.sleep(1)

async def main():
    log("main: start")
    t1 = asyncio.create_task(fetcher())
    t2 = asyncio.create_task(monitor())
    await asyncio.gather(t1, t2)

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    asyncio.run(main())
else:
    loop.create_task(main())
