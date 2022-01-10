#!/usr/bin/env python

import sys
import logging
import chembl_downloader
import time
import pandas as pd
from tqdm import tqdm
from rdkit.rdBase import BlockLogs
from descriptastorus.descriptors.DescriptorGenerator import MakeGenerator


class DescriptorCalc:
    def __init__(self):
        self.generator = MakeGenerator(("RDKit2D",))

    def from_smiles(self,smiles):
        # n.b. the first element is true/false if the descriptors were properly computed
        results = self.generator.process(smiles)
        if results is None:
            logging.warning("Unable to process smiles %s", smiles)
            return None
        processed, features = results[0], results[1:]
        if processed is None:
            logging.warning("Unable to process smiles %s", smiles)
            return None
        return features

    
if __name__ == "__main__":
    sql = """
    select canonical_smiles, cs.molregno, cx_logd
    from compound_structures cs
    join compound_properties cp on cs.molregno = cp.molregno
    """
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} outfile.pkl")
        sys.exit(2)

    outfile_name = sys.argv[1]
    start = time.time()
    tqdm.pandas()
    dc = DescriptorCalc()
    df = chembl_downloader.query(sql)
    df.columns = ["smiles","name","logd"]
    df['desc'] = df.smiles.progress_apply(dc.from_smiles)
    df.to_pickle(outfile_name)
    elapsed = time.time() - start
    rows, cols = df.shape
    num_desc = len(df.desc[0])
    print(f"{elapsed:.2f} s to calculate {num_desc} descriptors for {rows} molecules")
    print(f"Results written to {outfile_name}")


