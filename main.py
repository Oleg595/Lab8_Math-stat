import numpy as np
import scipy.stats as sts
import math

def average(x, size):
    num = 0.
    for i in x:
        num += i
    num /= size
    return num

def despertion(x, size):
    y = average(x, size)
    result = 0.
    for i in x:
        result += (i - y) * (i - y)
    result /= size
    return result

def student(x_av, s, alpha, n):
    result = np.zeros(2)
    result[0] = x_av - (s * sts.t.ppf((1 - alpha / 2), (n - 1))) / math.sqrt(n - 1)
    result[1] = x_av + (s * sts.t.ppf((1 - alpha / 2), (n - 1))) / math.sqrt(n - 1)
    return result

def chi_2(s, alpha, n):
    result = np.zeros(2)
    result[0] = (s * math.sqrt(n)) / math.sqrt(sts.chi2.ppf((1 - alpha / 2), (n - 1)))
    result[1] = (s * math.sqrt(n)) / math.sqrt(sts.chi2.ppf((alpha / 2), (n - 1)))
    return result

def m4_val(x, size):
    x_av = average(x, size)
    result = 0.
    for i in range(size):
        result += (x[i] - x_av) ** 4
    result /= size
    return result

def e_val(x, size):
    m4 = m4_val(x, size)
    s4 = despertion(x, size) ** 2
    result = (m4 / s4) - 3
    return result

def U_val(x, size, alpha):
    u_al = np.quantile(x, 1 - alpha / 2)
    e = e_val(x, size)
    result = u_al * math.sqrt((e + 2) / size)
    return result

def asym_sigma(x, size, alpha):
    U = U_val(x, size, alpha)
    s = math.sqrt(despertion(x, size))
    result = np.zeros(2)
    result[0] += s * (1 - 0.5 * U)
    result[1] += s * (1 + 0.5 * U)
    return result

def asym_mu(x, size, alpha):
    u_al = np.quantile(x, 1 - alpha / 2)
    x_av = average(x, size)
    s = math.sqrt(despertion(x, size))
    result = np.zeros(2)
    result[0] = x_av - (s * u_al) / math.sqrt(size)
    result[1] = x_av + (s * u_al) / math.sqrt(size)
    return result

arr = [20, 100]
alpha = 0.05

for i in arr:
    x = np.random.normal(0, 1, i)
    x_av = average(x, i)
    s = math.sqrt(despertion(x, i))
    stud = student(x_av, s, alpha, i)
    chi = chi_2(s, alpha, i)
    print("Num points =", i)
    print(stud[0], "< mu <", stud[1])
    print(chi[0], "< sigma <", chi[1])
    print()
    print("Asymptotic:")
    mu = asym_mu(x, i, alpha)
    sigma = asym_sigma(x, i, alpha)
    print(mu[0], "< mu <", mu[1])
    print(sigma[0], "< sigma <", sigma[1])
    print()
