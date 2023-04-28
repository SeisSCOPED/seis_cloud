import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import time
import os
import obspy
from scipy.fftpack import fft, fftfreq, next_fast_len
from obspy.clients.fdsn import Client
# The S3 stuff
import boto3
from botocore import UNSIGNED
from botocore.config import Config


client = Client("SCEDC")
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))


# where the data is
BUCKET_NAME = 'scedc-pds'

# where to put the daata
os.makedirs('./data' , exist_ok=True)


net = "CI"
sta = "RIO"
chan = "HHZ"
loc = "*"
year = 2022
mt = 5
day = 9
t0 = datetime.datetime( year , mt , day)
doy = int(t0.strtime("%j"))  # calculate the day of year
fmin = 0.1  # mininmum frequenc of the bandpass
fmax = 10   # maximum frequency band

tt0 = obspy.UTCDateTime( year , mt ,day)
fmin = 0.1  # m
fmax = 10   # maximum frequency band


# get data from seb services
t0 = time()
st1=client.get_waveforms(network = net ,station=sta ,location=loc ,channel=chan ,\
                       starttime=tt0 ,endtime=t0+86400)
t1=time()
print("Download time webservices %f", (t1-t0))

# define the file name
file = net+sta+'__'+chan+'___'+str(year)+str(doy).zfill(3)+'.ms'
# Key defined by SCEDC bucket
KEY = 'continuous_waveforms/2017/2017_180/'+file


# download data
t0 = time()
s3.Bucket(BUCKET_NAME).download_file(KEY, './data/' + file)
t1 = time()
print("Download time %f", (t1-t0))

# Compare with webservices



# Feature selection
st = obspy.read('./data/' + file)
st.filter('bandpass', freqmin = fmin, freqmax = fmax)
plt.plot(st[0].times(), st[0].data)
plt.savefig('test.png')

# get the maximum value in that frequency band
Amax = np.max(np.abs(st[0].data))
imax = np.argmax(np.abs(st[0].data))
Amaxt = st[0].times(type='timestamp')[imax]  # this is timestamps since POSIX time (197-,1,1).
print( Amax , Amaxt)



# 2. Fourier Transform
npts = st[0].stats.npts
# FFT the signals
# fill up until 2^N value to speed up the FFT
Nfft = next_fast_len(int(st[0].data.shape[0])) # this will be an even number
freqVec = fftfreq(Nfft, d=st[0].stats.delta)[:Nfft//2]
st.taper(max_percentage=0.05)
Zhat = fft(st[0].data , n=Nfft)

# fig,ax=plt.subplots(1,1,figsize=(11,8))
# ax.plot(freqVec,np.abs(Zhat[:Nfft//2])/Nfft)
# ax.grid(True)
# ax.set_xscale('log');ax[0].set_yscale('log')
# ax.set_xlabel('Frequency (Hz)');ax[0].set_ylabel('Amplitude (m/s)')
# plt.show()

imax = np.argmax(np.abs(Zhat[:Nfft//2]/Nfft))
Fmax = imax*st[0].stats.sampling_rate/2/Nfft
print(Fmax)

D = {'network':net,'station':sta,'channel':chan,'location':loc,\
     'freqmin':[fmin],'freqmax':[fmax],'date':[Amaxt],'Fmax':[Fmax]}
print(D)
print(Amaxt)


df=pd.DataFrame.from_dict(D)
df.to_csv('features.csv')



