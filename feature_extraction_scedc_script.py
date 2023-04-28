import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from time import time
import os
import obspy
from scipy.fftpack import fft, fftfreq, next_fast_len
from obspy.clients.fdsn import Client
# The S3 stuff
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# Configure clients to query from webservices and from S3
# FDSN - webservice client
client = Client("SCEDC")

# S3 - SCEDC data bucket
BUCKET_NAME = 'scedc-pds'
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))

# where to put the data & outputs
os.makedirs('./data' , exist_ok=True)
os.makedirs('./output' , exist_ok=True)

# Configure the data query below
net = "CI"
sta = "RIO"
chan = "HHZ"
loc = "*"
year = 2022
mt = 5
day = 9

t0 = datetime.datetime( year , mt , day)     # date time object
doy = int(t0.strftime("%j"))                  # calculate the day of year
tt0 = obspy.UTCDateTime( year , mt ,day)     # Obspy datetime object

# define the file name accordint
file = net+sta+'__'+chan+'___'+str(year)+str(doy).zfill(3)+'.ms'

fmin = 0.1  # mininmum frequenc of the bandpass
fmax = 10   # maximum frequency band

# get data from seb services
# Test query data from SCEDC webservices. 


t0 = time()
st1=client.get_waveforms(network = net ,station=sta ,location=loc ,channel=chan ,\
                       starttime=tt0 ,endtime=tt0+86400)
st1.write(file[:-1]+"seed",fmt="mseed")     # this step is not necessary for the analysis but necessary to compare with the download time with S3
t1=time()
print(f"Download time webservices takes {(t1-t0)}  s")

# Test query data from S3 bucket. We need to know the file structure of the SCEDC bucket

os.system("aws s3 ls --no-sign-request s3://scedc-pds/")
os.system("aws s3 ls --no-sign-request s3://scedc-pds/continuous_waveforms/")


# Key defined by SCEDC bucket
KEY = 'continuous_waveforms/'+str(year)+'/'+str(year)+'_'+str(doy).zfill(3)+'/'+file


# download data
t0 = time()
s3.Bucket(BUCKET_NAME).download_file(KEY, './data/' + file)
t1 = time()
print(f"Download time from S3 takes {(t1-t0)} s")
# this would be better if could stream in memory and save into disk

# Feature selection
t0=time()
st = obspy.read('./data/' + file)
t1=time()
print(f"reading time from local storage takes  {(t1-t0)} s")
st.filter('bandpass', freqmin = fmin, freqmax = fmax)
plt.plot(st[0].times(), st[0].data)
plt.savefig('./output/test.png')

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

imax = np.argmax(np.abs(Zhat[:Nfft//2]/Nfft))
Fmax = imax*st[0].stats.sampling_rate/2/Nfft
print(Fmax)

# Save extracted features into a DataFrame and Pandas

D = {'network':net,'station':sta,'channel':chan,'location':loc,\
     'freqmin':[fmin],'freqmax':[fmax],'date':[Amaxt],'Fmax':[Fmax]}
print(D)
print(Amaxt)


df=pd.DataFrame.from_dict(D)
df.to_csv('./output/features.csv')

# To download the data from EC2 to your local, you have two options:

# 1. From the jupyter notebook webpage, you can right click on the file and download. This is the easiest option when you are doing a manual download of a few files.
# 2. For larger requests, you have to use ```scp```. For this, open a new terminal and type:
#         cd the_directory_where_your_pem_or_ppk_file_is
#         scp -i "yourkeycredentials.pem" ec2-user@ec2-ip.amazon.com:/home/ec2-user/seis_cloud/outouts ~/yourchoiceofpath/