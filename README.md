# Cloud Computing for seismology 101

This repository is a minimum seismo-code to run on the cloud.

## Installation

You can install the package and the source codes as follow:
```bash
conda create -y -n seiscloud python=3.8 pip
conda activate seiscloud
pip install -r requirements.txt
```

You can also use ``Docker`` using the following commands:


__Warnings__: Right now the Dockerfile does not do anything ;-)
```bash
docker pull ghcr.io/seisscoped/seis_cloud:latest
docker run -v ${pwd}:/tmp -p 8888:8888 ghcr.io/seisscoped/seis_cloud:latest
```




# Tutorial documentation and links:

Getting on a AWS Instance in the [HPS JupyterBook](https://seisscoped.org/HPS/softhardware/AWS_101.html).


# Run the scripts

You can run a python scripts on the terminal interface of the instance by simply installing the packages (tutorials listed above):

```bash
python feature_extraction_script.py
```

You can also open a jupyter notebook and run the notebooks. Use the tutorials listed above and use ``feature_extraction_scedc_script.ipynb``.