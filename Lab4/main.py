from scipy.io import wavfile
import math

def openwave(filename):
    fs, data = wavfile.read(filename)
    return data

def DFT(data):
    res = []
    N = len(data)
    for k in range(N):
        summ = 0
        for n in range(N):
            summ += data[n]*math.exp(1)**complex(0, -2*math.pi*k*n/N)
        res.append(summ)
    return res

def invertDFT(data):
    res = []
    N = len(data)
    for n in range(N):
        summ = 0
        for k in range(N):
            summ += data[k]*math.exp(1)**complex(0, 2*math.pi*k*n/N)
        res.append(round((summ/N).real))
    return res


def w_ham(n, N): #hamming
    return 0.54 - 0.46 * math.cos(2*math.pi*n/N)


def windowDFT(data, w=1000):
    res = []
    N = len(data)
    if N < w:
        w = N
    start = 0
    for n in range(N):
        summ = 0
        for m in range(min(start, N-w), min(start+w, N)):
            summ += data[m] * w_ham(n-m, N) * math.exp(1)**(complex(0, -2*math.pi*n*m/N))
        res.append(summ)
        start += 1
    return res

