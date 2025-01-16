import time
import common.process as process

fonctions = []

def registerTicked(func, ticksNum):
    fonctions.append((func, ticksNum, 0))

def initClock():
    tick_interval = 1 / 50
    tick_count = 0
    while process.get_process_running_status("server-clock"):
        current_time = time.time()
        for i, (func, ticks, last_called_tick) in enumerate(fonctions):
            if tick_count - last_called_tick >= ticks:
                func()
                fonctions[i] = (func, ticks, tick_count)
        tick_count += 1
        time.sleep(tick_interval)
