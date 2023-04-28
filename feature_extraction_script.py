# This simple script will download 1 day of data from 1 station using
# webservices. The feature extracted are stored in a local CSV file
# and a plot of the data is saved into a PNG file.


# import modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fftpack import fft, fftfreq, next_fast_len
import obspy
from obspy.clients.fdsn import Client


# define FDSN client
client = Client("SCEDC")

net = "CI"
sta = "RIO"
chan = "HHZ"
loc = "*"
year = 2022
mt = 5
day = 9

fmin = 0.1  # minimum frequency band
fmax = 10   # maximum frequency band

# define obspy datetime object

t0 = obspy.UTCDateTime(year, mt, day)


# download data
st = client.get_waveforms(network=net, station=sta , location=loc, channel=chan, \
                       starttime=t0-1800, endtime=t0+86400)

# Now we extract 2 kinds of feature: 
# 1. Peak amplitude at a specific frequency band
# 2. Peak frequency of the Fourier Amplitude Spectrum
# We save the data into a CSV file that we will download.

st.filter('bandpass', freqmin=fmin, freqmax=fmax)
plt.plot(st[0].times(), st[0].data)
plt.savefig('./output/test.png')

# get the maximum value in that frequency band
Amax = np.max(np.abs(st[0].data))
imax = np.argmax(np.abs(st[0].data))
Amaxt = st[0].times(type='timestamp')[imax] # this is timestamps since POSIX time (197-,1,1).
print(Amax, Amaxt)

# 2. Fourier Transform
npts = st[0].stats.npts
# FFT the signals
# fill up until 2^N value to speed up the FFT
Nfft = next_fast_len(int(st[0].data.shape[0])) # this will be an even number
freqVec = fftfreq(Nfft, d=st[0].stats.delta)[:Nfft//2]
st.taper(max_percentage=0.05)
Zhat = fft(st[0].data, n=Nfft)

imax = np.argmax(np.abs(Zhat[:Nfft//2]/Nfft))
Fmax = imax*st[0].stats.sampling_rate/2/Nfft
print(Fmax)

D = {'network': net, 'station': sta, 'channel': chan, 'location': loc,\
     'freqmin': [fmin], 'freqmax': [fmax], 'date': [Amaxt], 'Fmax': [Fmax]}
print(D)
print(Amaxt)


df = pd.DataFrame.from_dict(D)
df.to_csv('./output/features.csv')



