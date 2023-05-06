# Cloud Computing for seismology 101

This repository is a minimum seismo-code to run on the cloud.

## Installation

You can install the package and the source codes as follow:
```bash
conda create -y -n seiscloud python=3.8 pip
conda activate seiscloud
pip install -r requirements.txt
```

You can also use ``Docker`` using the following commands. First pull the image using,
```bash
docker pull ghcr.io/seisscoped/seis_cloud:latest
```
To use Docker to run one script within the image in a single command line, you can type:
```bash
docker run -v ${pwd}:/tmp -p 8888:8888 ghcr.io/seisscoped/seis_cloud:latest python feature_extraction_scedc_script.py
```
where the ``-v ${pwd}:/tmp`` option mounts a local drive, ``-p 8888:8888`` will allow to open the jupyter notebook in a local port.


To run interactively and be prompted to the repository with the files, run:
```bash
docker run -it ghcr.io/seisscoped/seis_cloud:latest
```




# Tutorial documentation and links:

Getting on a AWS Instance in the [HPS JupyterBook](https://seisscoped.org/HPS/softhardware/AWS_101.html).


# Run the scripts

You can run a python scripts on the terminal interface of the instance by simply installing the packages (tutorials listed above):

```bash
python feature_extraction_scedc_script.py
```

You can also open a jupyter notebook and run the notebooks. Use the tutorials listed above and use ``feature_extraction_scedc_script.ipynb``.
