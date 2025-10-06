import click
import pystow

SFI_MODULE = pystow.module("PatWalters", "sfi")
LATEST_LOGD_CHEMBL_VERSION = "35"

def validate_chembl_version(_ctx, _param, value):
    """Validate that ChEMBL version is <= 35 (due to schema changes in v36+)"""
    if value is None:
        return "35"  # Default to 35; 36 deprecates logd

    try:
        version_num = int(value)
        if version_num > 35:
            raise click.BadParameter(f"ChEMBL version {version_num} is not supported. Please use version 35 or earlier due to database schema changes.")
        return str(version_num)
    except ValueError:
        raise click.BadParameter(f"Invalid ChEMBL version: {value}. Must be a number <= 35.")

chembl_version_option = click.option(
    "--chembl-version",
    default=LATEST_LOGD_CHEMBL_VERSION,
    callback=validate_chembl_version,
    help="ChEMBL version to use (must be <= 35 due to schema changes)"
)
