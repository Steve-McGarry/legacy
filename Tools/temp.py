# %%
ext = 15.6
import time

# %%
counter = 1
while True:
    while counter != 10:
        print(f'General loop {counter}')
        print(ext)
        counter += 1
        time.sleep(1)
    counter = 1
    ext += 1
# %%
