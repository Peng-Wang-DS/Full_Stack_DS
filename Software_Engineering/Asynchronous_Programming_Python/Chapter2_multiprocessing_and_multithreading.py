
# %% Single-process solution 
from math import (asin,sin,cos,pi,sqrt)
from typing import List, Tuple
from numbers import Number

def cities_into_tuples(cities: List) -> List:
    cities_list = []
    total_cities = len(cities)
    for i in range(0, total_cities):
        if i + 1 < total_cities:
         cities_list.append((cities[i], cities[i + 1],))
    return cities_list

def great_circle_distance(src_dest: Tuple) -> Number:
    source = src_dest[0]
    dest = src_dest[1]
    lat1 = abs(float(source['lat']) * pi / 180)
    lat2 = abs(float(dest['lat']) * pi / 180)
    lon1 = abs(float(source['lng']) * pi / 180)
    lon2 = abs(float(dest['lng']) * pi / 180)
    distance = 2 * asin(sqrt((sin((lat1 - lat2) / 2))**2 +
    cos(lat1) * cos(lat2) * (sin((lon1 - lon2) / 2))**2))
    distance = distance * 180 * 60 / pi
    return distance

def calculate_path_distance(cities: List) -> Number:
    total = 0
    for t in cities:
        d = great_circle_distance(t)
        print(f"From: {t[0]['city_ascii']} to: {t[1]['city_ascii']},distance: {d} nm")
        total = total + d
    return total

import time
start_time = time.time()
cities = [
    {"city_ascii": "New York", "lat": 40.7128, "lng": -74.0060},
    {"city_ascii": "Los Angeles", "lat": 34.0522, "lng": -118.2437},
    {"city_ascii": "Chicago", "lat": 41.8781, "lng": -87.6298},
    {"city_ascii": "Houston", "lat": 29.7604, "lng": -95.3698},
    {"city_ascii": "Phoenix", "lat": 33.4484, "lng": -112.0740},
    {"city_ascii": "Philadelphia", "lat": 39.9526, "lng": -75.1652},
    {"city_ascii": "San Antonio", "lat": 29.4241, "lng": -98.4936},
    {"city_ascii": "San Diego", "lat": 32.7157, "lng": -117.1611},
    {"city_ascii": "Dallas", "lat": 32.7767, "lng": -96.7970},
    {"city_ascii": "San Jose", "lat": 37.3382, "lng": -121.8863},
]


tuples = cities_into_tuples(cities)
calculate_path_distance(tuples)
end_time = time.time()
print(f"taken {end_time-start_time}s")






# %% multi-threading non-safe example
import time
import threading
lock = threading.Lock()
def add_to_total():
    # name = threading.current_thread().name
    global total
    for i in range(1000):
        # with lock:
        curr = total
        time.sleep(0)  # simulate i/o task
        # if total != curr:
            # print(f"[{name}] RACE: total changed from {curr} to {total} before write")
        curr += 1
        total = curr
        
total = 0
threads = []

for i in range(2):
    t = threading.Thread(target=add_to_total,name=f'Thread{i}')
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f'{total=}')

print(f"the correct result should be {sum(1 for _ in range(1000))*2}")



# %% implement multi-threading via joblib - use lock
total = 0
threads = []
import threading
import time
lock = threading.Lock()
def add_to_total(x):
    global total
    for i in range(1000):
        with lock:
            curr = total
            time.sleep(0)  # simulate i/o task
            curr += 1
            total = curr
        
from joblib import Parallel, delayed
Parallel(n_jobs=-1, backend='threading')(delayed(add_to_total)(x) for x in range(2)) 

print(total)


# %% implement multi-threading via joblib - avoid global variable
import time 
def evaluate_execution_time(fn):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        output = fn(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        time_tracker = (fn.__name__, time_taken)
        
        print(f"\033[92mCompleted {time_tracker[0]} in {time_tracker[1]}s\033[0m")
        return time_tracker, output
    return wrapper
    
import threading
total = 0
threads = []


def add_to_total(x):
    name = threading.current_thread().name
    curr = 0
    print(f"Running Thread{name}...")
    time.sleep(3)
    for i in range(1000):
        curr += 1
    return curr

@evaluate_execution_time
def run_joblib1():
    results = Parallel(n_jobs=-1, backend='threading')(delayed(add_to_total)(x) for x in range(4))
    return results


time_tracker, output = run_joblib1()
print(output)


# %% implement multi-processing via joblib - avoid global variable
import time 
def evaluate_execution_time(fn):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        output = fn(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        time_tracker = (fn.__name__, time_taken)
        
        print(f"\033[92mCompleted {time_tracker[0]} in {time_tracker[1]}s\033[0m")
        return time_tracker, output
    return wrapper
    
import threading
total = 0
threads = []


def add_to_total(x):
    curr = 0
    time.sleep(3)
    for i in range(1000):
        curr += 1
    return curr

@evaluate_execution_time
def run_joblib1():
    results = Parallel(n_jobs=-1, backend='loky')(delayed(add_to_total)(x) for x in range(4))
    return results


time_tracker, output = run_joblib1()
print(output)


# %% implement multi-processing via ray 

import time 
from functools import wraps

def evaluate_execution_time(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        start_time = time.time()
        output = fn(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        time_tracker = (fn.__name__, time_taken)
        
        print(f"\033[92mCompleted {time_tracker[0]} in {time_tracker[1]}s\033[0m")
        return time_tracker, output
    return wrapper
    
total = 0
threads = []

import ray 
ray.init()


@ray.remote
def add_to_total(x):
    curr = 0
    time.sleep(3)
    for i in range(1000):
        curr += 1
    return curr


@evaluate_execution_time
def run_ray1():
    futures = [add_to_total.remote(x) for x in range(4)]
    results = ray.get(futures)
    return results

output = run_ray1()
print(output)
ray.shutdown()


run_joblib1.__name__


