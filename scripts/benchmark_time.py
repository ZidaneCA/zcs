import time
import matplotlib.pyplot as plt
import os


def benchmark(length=10):
    total_time = 0
    readings = []
    while total_time < length:
        start = time.time()
        readings.append(time.time())
        time.sleep(0.1)
        end = time.time()
        total_time += (end - start)
    readings.append(total_time)
    print("Exec time: ", readings[-1])
    return readings


def bench_plot(exec_time):
    y, et, x = ([] for i in range(3))
    clock_sources = ['acpi_pm', 'hpet', 'zcs', 'tsc']
    for i in range(4):
        os.system("sudo bash -c 'echo " + clock_sources[i] + "> /sys/devices/system/clocksource/clocksource0"
                                                             "/current_clocksource'")
        y.append(benchmark(exec_time))
        et.append(y[i][-1] - exec_time)
    n = len(y[0])
    for i in range(n):
        x.append(i)
    # Plotting of GRAPHS
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Execution times')
    ax1.bar(clock_sources, et)
    for i in range(4):
        ax2.plot(x[:n - 1], y[i][:n - 1], label=clock_sources[i])
    plt.xlabel('Count')
    plt.ylabel('Time values')
    plt.title('Time values for various clock sources')
    plt.legend()
    plt.show()


bench_plot(10)
