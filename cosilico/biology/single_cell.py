import altair as alt

import cosilico.base as base


def qc_histogram(adata, variables, width=700):
    """Display QC variables for the given single cell data as a histogram

    Arguments
    ---------
    adata : anndata.AnnData
        AnnData object holding single cell expression data.
    variables : Collection
        List of variables to include in the plot
    width : int
        Width of chart

    Example
    -------
    >>> from cosilico.datasets import helpers
    >>> from cosilico.biology import single_cell
    >>>
    >>> adata = helpers.raw_pbmc()
    >>>
    >>> single_cell.qc_histogram(adata,
    ...     ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'])
    >>>

    Returns
    -------
    altair.Chart
    """
    chart = None
    for var in variables:
        histogram = base.histogram(var, adata.obs, maxbins=50)
        histogram = histogram.properties(width=int(width / len(variables)))
        if chart is None:
            chart = histogram
        else:
            chart |= histogram
    return chart


def qc_scatter(adata, x, variables, width=700, hist_height=100):
    """Display QC variables for the given single cell data as a
    scatter plot.

    Arguments
    ---------
    adata : anndata.AnnData
        AnnData object holding single cell expression data.
    x : str
        Variable for x-axes. 
    variables : Collection
        List of variables for y-axes. Must be in adata.obs
    width : int
        Width of chart
    hist_height : int
        Height of histograms

    Example
    -------
    >>> from cosilico.datasets import helpers
    >>> from cosilico.biology import single_cell
    >>>
    >>> adata = helpers.raw_pbmc()
    >>>
    >>> single_cell.qc_scatter(adata, 'total_counts',
    ...     ['pct_counts_mt', 'n_genes_by_counts'])
    >>>

    Returns
    -------
    altair.Chart
    """
    chart = None
    for var in variables:
        scatter = base.scatterplot(x, var, adata.obs)
        scatter = scatter.properties(width=int(width / len(variables)))
        histogram = base.histogram(x, adata.obs, maxbins=50, color='orange')
        histogram = histogram.properties(width=int(width / len(variables)),
            height=hist_height)
        scatter = alt.vconcat(scatter, histogram).resolve_scale(x='shared')
        if chart is None:
            chart = scatter
        else:
            chart |= scatter
    return chart

