from main import *

data = openwave('4.wav')
L = data[:, 0]
R = data[:, 1]

mobj = Mlaw(L)
print('M-law')
print(mobj.signal_myu_encoded)
print('------------------------------')
print('------------------------------')
print('------------------------------')

aobj = Alaw(L)
print('A-law')
print(aobj.signal_a_encoded)
