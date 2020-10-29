import os
import pkg_resources
import re

import anndata

def raw_pbmc():
    """Load raw 10x pbmc count data as a anndata.AnnData object

    Downloaded from http://cf.10xgenomics.com/samples/cell-exp/1.1.0/\
            pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz

    Has had QC metrics calculated based on the scanpy clustering 
    tutorial found here
    https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html.
    The following are the scanpy functions run on the dataset.

    Filtering steps:
    - sc.pp.filter_cells(adata, min_genes=200)
    - sc.pp.filter_genes(adata, min_cells=3)

    QC metrics:
    - adata.var['mt'] = adata.var_names.str.startswith('MT-')
    - sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'],
            percent_top=None, log1p=False, inplace=True)

    Example
    -------
    >>> from cosilico.datasets import helpers
    >>> adata = helpers.raw_pbmc()

    Returns
    -------
    anndata.AnnData

    """
    fp = pkg_resources.resource_filename('cosilico',
            'datasets/data/raw_pbmc.h5ad')
    return anndata.read_h5ad(fp)
