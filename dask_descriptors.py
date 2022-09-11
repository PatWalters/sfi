#!/usr/bin/env python

import os
import sys
import time
from pathlib import Path
from typing import Optional

import chembl_downloader
import click
import dask.dataframe as dd
import pystow
import useful_rdkit_utils as uru
from dask.diagnostics import ProgressBar
from constants import SFI_MODULE, chembl_version_option


def df_prop(df_in):
    rdkit_desc = uru.RDKitDescriptors()
    return df_in.smiles.apply(rdkit_desc.calc_smiles)


def get_chembl_logd_data(chembl_version: Optional[str] = None):
    sql = """
    select canonical_smiles, cs.molregno, cx_logd
    from compound_structures cs
    join compound_properties cp on cs.molregno = cp.molregno
    """
    df = chembl_downloader.query(sql, version=chembl_version)
    df.columns = ["smiles", "name", "logd"]
    return df


@click.command()
@chembl_version_option
@click.option("--num-cores", type=int, default=lambda: os.cpu_count() - 1)
def main(chembl_version: str, num_cores: int):
    outfile_name = SFI_MODULE.join(chembl_version, name="logd_descriptors.pkl")

    start = time.time()
    print(f"Reading ChEMBL {chembl_version} data")
    df = get_chembl_logd_data(chembl_version=chembl_version)
    print("Done")

    print(f"Calculating properties with {num_cores} cores")
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
