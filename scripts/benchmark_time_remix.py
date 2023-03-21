import threading
import time
import matplotlib.pyplot as plt
import os
from operator import add, mul, sub


class TimeThread(threading.Thread):
    def __init__(self, length):
        threading.Thread.__init__(self)
        self.length = length
        self.readings = []

    def run(self):
        total_time = 0
        while total_time < self.length:
            start = time.time()
            self.readings.append(time.time())
            time.sleep(0.1)
            end = time.time()
            total_time += (end - start)
        self.readings.append(total_time)
        print("Exec time: ", self.readings[-1])

    def join(self):
        threading.Thread.join(self)
        return self.readings  # add exec time (total_time) to returned value


def bench_plot(exec_time):
    summ, avg, diff, et, x, readings, variability = ([] for i in range(7))
    clock_sources = ['acpi_pm', 'hpet', 'zcs', 'tsc']
    for i in range(4):
        os.system("sudo bash -c 'echo " + clock_sources[i] + "> /sys/devices/system/clocksource/clocksource0"
                                                             "/current_clocksource'")
        # Creation of thread(s)
        time_thread_one = TimeThread(exec_time)
        time_thread_two = TimeThread(exec_time)
        time_thread_three = TimeThread(exec_time)
        time_thread_four = TimeThread(exec_time)
        # Starting of Thread(s)
        time_thread_one.start()
        time_thread_two.start()
        time_thread_three.start()
        time_thread_four.start()
        readings.append(
            [time_thread_one.join(), time_thread_two.join(), time_thread_three.join(), time_thread_four.join()])
    n = len(readings[0][0])
    for i in range(4):  # four here is number of clocksources
        et.append([])
        diff.append([])
        variability.append([])
        sum_tmp = n * [0]
        avg_tmp = n * [0]
        for j in range(4):  # 4 here is for number of threads
            et[i].append(readings[j][i][-1] - exec_time)
            sum_tmp = list(map(add, sum_tmp, readings[i][j]))  # sum of all the readings from various threads j in clocksource i
        summ.append(sum_tmp)  # summ[i] is sum of readings of a all threads in clocksource i
        avg_tmp = [m / 4 for m in summ[i]]
        avg.append(avg_tmp)  # avg[i] corresponds to clocksource i
        # Calculating Average difference and variability
        for k in range(4):  # 4 here is for number of threads
            diff[i].append(list(map(sub, readings[i][k], avg[i])))  # diff[i][j] is difference between readings of thread j and average for clocksource i
            variability[i].append(list(map(add, diff[i][k], readings[i][k])))
    # as of here, readings[i][j] is thread j for clocksource i whereas et[i][j] are execution times for thread i in clocksource j.
    for i in range(n):
        x.append(i)
    fig, ax1, ax2 = ([0] * 4 for j in range(3))
    for i in range(4):
        fig[i], (ax1[i], ax2[i]) = plt.subplots(2)
        fig[i].suptitle('Execution time thread ' + str(i))
        ax1[i].bar(clock_sources, et[i])
        for j in range(4):
            ax2[i].plot(x[:n - 1], readings[j][i][:n - 1], label=clock_sources[j])
            ax2[i].plot(x[:n - 1], variability[j][i][:n - 1], label="variability "+clock_sources[j], linestyle="dashed")
    plt.xlabel('Count')
    plt.ylabel('Time values')
    plt.title('Time values for various clock sources')
    plt.legend()
    plt.show()


bench_plot(10)
