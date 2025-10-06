#!/usr/bin/env python

from sfi_predictor import SFIPredictor
from rdkit import Chem
import click
import pandas as pd
from constants import chembl_version_option
from constants import SFI_MODULE


@click.command()
@click.argument("csv")
@click.option("--smiles-column", default="smiles")
@click.option("--out-csv", default="computed_SFIs.csv")
@chembl_version_option
def main(csv, smiles_column, chembl_version, out_csv):
    path = SFI_MODULE.join(chembl_version, name="model.txt")
    sfi_predictor = SFIPredictor(path)
    df = pd.read_csv(csv)
    df["SFI"] = df[smiles_column].apply(sfi_predictor.predict_smiles)
    print(df)
    df.to_csv(out_csv, index=False)


if __name__ == "__main__":
    main()
