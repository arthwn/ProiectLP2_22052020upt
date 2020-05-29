import wave
import struct
import math


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while True:
    try:
        file = input('Nume fisier .wav:')
        fisier_wav = wave.open(file, 'rb')
        break
    except FileNotFoundError:
        print("Fisierul nu a fost gasit")
        
(nchannels, sampwidth, framerate, nframes, comptype, compname) = fisier_wav.getparams()

def intrare():

    data = fisier_wav.readframes(nframes)
    data = struct.unpack('<{n}h'.format(n=nframes), data)

    data = list(data)
    return data

data_init = intrare()
fisier_wav.close()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def proc(f_centrala, bandwidth, gain, data):
    p = gain/40
    A = math.pow(10,p)
    w0 = 2*math.pi*(f_centrala/(framerate))
    c = math.cos(w0)
    s = math.sin(w0)

    alpha = s*math.sinh((math.log(2)/2)*bandwidth*(w0/s))

    b0 = 1 + alpha*A
    b1 = -2*c
    b2 = 1 - alpha*A
    a0 = 1 + alpha/A
    a1 = -2*c
    a2 = 1 - alpha/A

    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0
    a0 = 1

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    out = list() 

    for x in data:
        y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    
        out.append(y)
    return out
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while True:
    print('EQ parametric:\n\n-15<Gain<15; 0.2<Bandwidth<7; 10<F. centr.<10000\n\n ')
    print('1-Default (Low,Mid,High)\n2-Custom')
    choice = int(input('Alegere:'))
    if choice == 1:
        #bdwtj = int(input('Bandwidth Joase:'))
        gj = int(input('Gain Joase:'))
        #bdwtm = int(input('Bandwidth Medii:'))
        gm = int(input('Gain Medii:'))
        #bdwti = int(input('Bandwidth Inalte:'))
        gi = int(input('Gain Inalte:'))
        if gj <-15 or gj >15 or gm < -15 or gm > 15 or gi < -15 or gi > 15:
            print('-15<Gain<15')
            continue
        
        mod1 = proc(150, 7, gj, data_init) 
        mod2 = proc(1000, 5, gm, mod1)
        modf = proc(5500, 3, gi, mod2)
        break
    
    elif choice == 2:
        f0 = int(input('Frecv. centrala:'))
        b = int(input('Bandwith:'))
        g = int(input('Gain:'))
        modf = proc(f0, b, g, data_init)
        break
    else:
        continue
        
    if 10>f0 or f0>10000 or 0.2>b or b>7 or -15>g or g>15:
        print("10<f0<10000; 0.2<b<7; -15<g<15")
        continue
        
outTup = tuple(modf)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
output = wave.open('output.wav', 'w')
output.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

for a in outTup:
    output.writeframes(struct.pack('h', int(a)))
    
output.close()


end = input('Fsierul output.wav a fost creat ')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

