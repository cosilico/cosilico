import altair as alt
import pandas as pd

def layered_histogram(x, hue, data, opacity=.6, maxbins=100):
    """Display a layered histogram.

    Parameters
    ----------
    x : str
        value to be binned
    hue : str
        value defining layers of the histogram
    data : pandas.DataFrame
        dataframe containing x and hue columns
    opacity : float
        opacity of the histogram layers
    maxbins : int
        max bins allowable in the histogram

    Example
    -------
    >>> from cosilico.base.distribution import layered_histogram
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>> layered_histogram('sepal_length', 'species', iris)

    Returns
    -------
    altair.Chart

    """
    chart = alt.Chart(data).mark_area(
        opacity=opacity,
        interpolate='step'
    ).encode(
        alt.X(f'{x}:Q', bin=alt.Bin(maxbins=100), title=x),
        alt.Y('count()', stack=None, title='Count'),
        alt.Color(f'{hue}:N')
    )

    return chart
