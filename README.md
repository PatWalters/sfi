## sfi

An implementation of the Solubility Forecast Index (SFI)

## Installation and Use
### Installation
The necessary libraries can be installed using the command below.
<pre>
pip install -r requirements.txt
</pre>

### The fast, easy way to calculate SFI 
The notebook **example_sfi.ipynb** shows how to use a stored cLogD model
to predict and plot SFI. 

### The slow way, if you want to see how the sausage if made

1. The script **dask_descriptors.py** extracts structures and cLogD data 
for more than 2 million molecules from the ChEMBL database and generates
molecular descriptors. The script uses the [chembl-downloader](https://github.com/cthoyt/chembl-downloader), so it's not 
necessary to have ChEMBL installed to run these scripts and notebooks. 
Note that running this script will take a while. On my MacBook Pro, this 
takes about 7hrs. **You have been warned**.
<pre>
dask_descriptors.py logd_descriptors.pkl
</pre>
2. The notebook **build_logd_model.ipynb** generates a machine learning model for predicting
cLogD based on the data in the ChEMBL database. This provides a nice example of how we can use 
LightGBM to generate a machine learning model for a large dataset. 
3. The notebook **example_sfi.ipynb** shows how to use a stored cLogD model
to predict and plot the Solubility Forecast Index (SFI). 
## Bibliography
Hill, A. P., & Young, R. J. (2010).
Getting physical in drug discovery: a contemporary perspective on solubility and hydrophobicity.
Drug discovery today, 15(15-16), 648-655.
https://doi.org/10.1016/j.drudis.2010.05.016
