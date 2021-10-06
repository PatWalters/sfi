#!/usr/bin/env python

import sys
import pandas as pd
from tqdm import tqdm
from descriptastorus.descriptors.DescriptorGenerator import MakeGenerator

# Read LogD data from ChEMBL, calculate descriptors, and save descriptors to a pickle file

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


