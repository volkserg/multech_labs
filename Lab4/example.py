from main import *


data = openwave('4.wav')
L = data[:, 0]
R = data[:, 1]

dat = [1, 2, 5, 7]
# dat = L

d = DFT(dat)

und = invertDFT(d)
# print(und)

print(d)
print(windowDFT(dat))