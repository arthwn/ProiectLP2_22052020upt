import numpy as np
import wave
import struct
#import matplotlib.pyplot as plt
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>INPUT>>>	
fisier_wav = wave.open('test.wav', 'r')
num_samples = fisier_wav.getnframes()
data = fisier_wav.readframes(num_samples)

data = struct.unpack('{n}h'.format(n=num_samples), data)
data = np.array(data)

data_transff = np.fft.fft(data)
frecv = np.abs(data_transff[:len(data_transff)])

print(frecv[1000])
print(frecv[970])

# plt.plot(frecv)
# plt.title('Fecvente inainte de modificare')
# plt.show()
# plt.close()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PROC>>>
index = 0


for f in frecv:
    
    if index > 950 and index < 1050:
        frecv[index] = frecv[index] + 100
        
    
        
    index += 1

	
print(frecv[1000])
print(frecv[970])

# plt.plot(frecv)
# plt.title("Frecvente dupa modificare")
# plt.xlim(0,1200)
# plt.show()
# plt.close()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>OUTPUT>>>
