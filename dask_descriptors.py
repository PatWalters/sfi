#!/usr/bin/env python

import sys
import time

import chembl_downloader
import dask.dataframe as dd
import useful_rdkit_utils as uru
from dask.diagnostics import ProgressBar


def df_prop(df_in):
    rdkit_desc = uru.RDKitDescriptors()
    return df_in.smiles.apply(rdkit_desc.calc_smiles)


def get_chembl_logd_data():
    sql = """
    select canonical_smiles, cs.molregno, cx_logd
    from compound_structures cs
    join compound_properties cp on cs.molregno = cp.molregno
    """
    df = chembl_downloader.query(sql)
    df.columns = ["smiles", "name", "logd"]
    return df


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} outfile.pkl")
        sys.exit(2)

    outfile_name = sys.argv[1]
    start = time.time()
    print("Reading ChEMBL data")
    df = get_chembl_logd_data()
    print("Done")

    print("Calculating properties")
    num_cores = 8
    ddf = dd.from_pandas(df, npartitions=num_cores)
    with ProgressBar():
        df["desc"] = ddf.map_partitions(df_prop, meta='float').compute(scheduler='processes')
    df.to_pickle(outfile_name)
    elapsed = time.time() - start
    rows, cols = df.shape
    num_desc = len(df.desc[0])
    print(f"{elapsed:.2f} s to calculate {num_desc} descriptors for {rows} molecules")
    print(f"Results written to {outfile_name}")


if __name__ == "__main__":
    main()
