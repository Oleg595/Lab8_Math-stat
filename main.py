import numpy as np
import matplotlib.pyplot as plt
from array import array
import math

def read_signal(str):
    data = []
    with open(str, 'r') as inf:
        for line in inf.readlines():
            remove_dirst_str = line.replace("[", "")
            remove_next_str = remove_dirst_str.replace("]", "")
            data.append(remove_next_str.split(", "))

    data_float_format = []
    for item in data:
        for x in item:
            data_float_format.append(float(x))
    return data_float_format

def get_array(data, num, size):
    result = np.zeros(size)
    for i in range(size):
        result[i] = data[(num - 1) * size + i]
    return result

def get_y(num):
    time_result = []
    time_result.append([float(x) for x in range(1, num + 1)])
    result = np.zeros(num)
    for i in range(num):
        result[i] = time_result[0][i]
    return result

def del_blowout(data, size):
    time_result = data
    for j in range(1, 3):
        for i in range(1, size - 1):
            if time_result[i] > (time_result[i + 1] + time_result[i - 1]) / 2:
                time_result[i] = (time_result[i + 1] + time_result[i - 1]) / 2
                j = i - 1
                while time_result[j] > (time_result[j + 1] + time_result[j - 1]) / 2:
                    time_result[j] = (time_result[j + 1] + time_result[j - 1]) / 2
                    j -= 1
    return time_result

def get_Areas(data, size):
    num = int(math.log2(size))
    hist = plt.hist(data, bins= num)
    plt.show()
    count = []
    start = []
    finish = []
    types = [0] * num
    for i in range(num):
        count.append(hist[0][i])
        start.append(hist[1][i])
        finish.append(hist[1][i + 1])
    sortCount = sorted(count)
    k = 0
    for i in range(num):
        for j in range(num):
            if int(sortCount[num - i - 1]) == int(count[j]):
                if k == 0:
                    types[j] = "Фон"
                elif k == 1:
                    types[j] = "Сигнал"
                else:
                    types[j] = "Переход"
                k += 1
    data = start, finish, types, count
    return data

def inta_group(data, size, k):
    result = 0
    num = int(size / k)
    for i in range(k):
        d = data[num * i: num * (i + 1)]
        n = np.mean(d)
        time_result = 0
        for i in range(num):
            time_result += (d[i] - n) ** 2
        time_result /= (k - 1)
        result += time_result
    result /= k
    return result

def inter_group(data, size, k):
    result = 0
    num = int(size / k)
    av = np.mean(data)
    for i in range(k):
        d = data[num * i: num * (i + 1)]
        n = np.mean(d)
        result += (n - av) ** 2
    result /= (k - 1)
    result *= k
    return result


def get_F(data, size, k):
    print("k =", k)
    inta = inta_group(data, size, k)
    print("inta group =", inta)
    inter = inter_group(data, size, k)
    print("inter group =", inter)
    print("inter / inta", inter / inta)


def get_k(size):
    k = 4
    while size % k != 0:
        k += 1
        if size == k:
            size += 1
            k = 4
    return k

def print_fisher(area_data, size, data):
    new_data = array("f", data)
    for i in range(size - 1):
        d = np.zeros(area_data[i + 1] - area_data[i])
        for j in range(area_data[i + 1] - area_data[i]):
            d[j] = new_data[area_data[i] + j]
        #d = data[area_data[i]: area_data[i + 1]]
        k = get_k(len(d))
        get_F(d, area_data[i + 1] - area_data[i], k)

def disturb(x, num, data, size):
    y = get_y(num)
    area_data = []
    label = []
    area_data.append(0)
    start = 0
    i = 0
    n = 0
    while i < num:
        for j in range(size):
            count = 0
            while i < num and x[i] <= data[1][j] and x[i] >= data[0][j]:
                count += 1
                i += 1
            if count > 0:
                label.append(data[2][j])
                n += 1
                area_data.append(int(start + count))
                start += count

    area_data = area_data, label
    new_data = []
    new_data.append(0)

    i = 0
    while i < n:
        if area_data[1][i] == "Фон":
            color_ = 'y'
        if area_data[1][i] == "Сигнал":
            color_ = 'r'
        if area_data[1][i] == "Переход":
            color_ = 'g'
        j = i + 1
        while j < n and area_data[1][j] == area_data[1][i]:
            j += 1
        plt.plot(y[int(area_data[0][i]):int(area_data[0][j])],
                 x[int(area_data[0][i]):int(area_data[0][j])], color=color_, label=area_data[1][i])
        new_data.append(area_data[0][j])
        i = j
    new_data = array("i", new_data)
    print_fisher(new_data, len(new_data), x)
    plt.legend()
    plt.show()

fileData = read_signal("wave_ampl.txt")
idSignal = 80
indArray = get_array(fileData, idSignal, 1024)
y = get_y(1024)

plt.plot(y, indArray)
plt.show()

plt.hist(indArray, bins=10, range=(min(indArray), max(indArray)), density=True)
plt.show()

newArray = del_blowout(indArray, 1024)
data = get_Areas(newArray, 1024)
plt.plot(y, newArray)
plt.show()
disturb(newArray, 1024, data, 10)
