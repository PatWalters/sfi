#!/usr/bin/env python

import sys
import pandas as pd
from tqdm import tqdm
from descriptastorus.descriptors.DescriptorGenerator import MakeGenerator

# Read LogD data from ChEMBL, calculate descriptors, and save descriptors to a pickle file
# Input data looks like this
# canonical_smiles,molregno,cx_logd
# Cc1cc(-n2ncc(=O)[nH]c2=O)ccc1C(=O)c1ccccc1Cl,1,2.69
# Cc1cc(-n2ncc(=O)[nH]c2=O)ccc1C(=O)c1ccc(C#N)cc1,2,1.82
# Cc1cc(-n2ncc(=O)[nH]c2=O)cc(C)c1C(O)c1ccc(Cl)cc1,3,2.64
# Cc1ccc(C(=O)c2ccc(-n3ncc(=O)[nH]c3=O)cc2)cc1,4,1.97

class DescriptorCalc:
    def __init__(self):
        self.generator = MakeGenerator(("RDKit2D",))

    def from_smiles(self,smiles):
        # n.b. the first element is true/false if the descriptors were properly computed
        results = self.generator.process(smiles)
        processed, features = results[0], results[1:]
        if processed is None:
            logging.warning("Unable to process smiles %s", smiles)
            # if processed is None, the features are are default values for the type
        return features

    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: infile.csv outfile.pkl")
        sys.exit(0)
        
    tqdm.pandas()
    dc = DescriptorCalc()
    df = pd.read_csv(sys.argv[1])
    df.columns = ["smiles","name","logd"]
    df['desc'] = df.smiles.progress_apply(dc.from_smiles)
    df.to_pickle(sys.argv[2])


