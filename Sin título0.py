import numpy as np
import matplotlib.pyplot as plt

def periodgram(t,signal):
    T = t[1]-t[0]
    
    fft_values = np.fft.fft(signal)
    N = len(signal)

    freq = np.fft.fftfreq(N, T)

    magnitude = np.abs(fft_values)
    
    plt.subplot(2, 1, 1)
    plt.plot(t, signal)
    plt.title('Time Domain Signal')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    
    plt.subplot(2, 1, 2)
    plt.stem(freq[:N//2], magnitude[:N//2])
    plt.title('Frequency Domain (Magnitude Spectrum)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.tight_layout()
    plt.show()
    
    return np.max(magnitude), np.argmax(magnitude), freq[np.argmax(magnitude)]

#Fs = 500 
#Ti = 1/Fs 
#t = np.arange(0, 1, Ti)  

#f1 = 50
#f2 = 120
#signal = 0.7*np.sin(2*np.pi*f1*t) + 1.0*np.sin(2*np.pi*f2*t)

t = np.arange(0, 20*np.pi, 0.01)

signal = np.sin(t)

a, b, c = periodgram(t,signal)

print(a, b, 1/c)

