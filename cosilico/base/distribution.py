from collections import Collection

import altair as alt
import pandas as pd


def histogram(x, data, opacity=1., maxbins=30, color=None, padding=0):
    """Display a histogram.

    Parameters
    ----------
    x : str
        value to be binned
    data : pandas.DataFrame
        dataframe containing x
    opacity : float
        opacity of the histogram layer
    maxbins : int
        max bins allowable in the histogram
    color : str, None
        Color of histogram layer
    padding : int
        Amount of padding on ends of x-axis

    Example
    -------
    >>> import cosilico.base as base
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.histogram('sepal_length', iris)

    Returns
    -------
    altair.Chart

    """
    configure_mark_kwargs = {
        'opacity': opacity,
    }
    if color is not None: configure_mark_kwargs['color'] = color

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{x}:Q',
            bin=alt.Bin(maxbins=maxbins),
            title=x,
            scale=alt.Scale(padding=padding)
        ),
        y=alt.Y('count():Q',
            title='Count',
        )
    ).configure_mark(**configure_mark_kwargs)

    return chart

def layered_histogram(x, hue, data, opacity=.6, maxbins=100,
        stack=None, padding=0):
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
    stack : str, None, bool
        argument for stack parameter in altair. If None,
        then the areas of the layers that overlap will be
        different colors. If 'zero', then the layers will
        completly occlude one another.
    padding : int
        Amount of padding on ends of x-axis

    Example
    -------
    >>> import cosilico.base as base
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.layered_histogram('sepal_length', 'species', iris)

    Returns
    -------
    altair.Chart

    """
    chart = alt.Chart(data).mark_area(
        opacity=opacity,
        interpolate='step'
    ).encode(
        alt.X(f'{x}:Q', bin=alt.Bin(maxbins=100), title=x,
            scale=alt.Scale(padding=padding)),
        alt.Y('count()', stack=stack, title='Count'),
        alt.Color(f'{hue}:N')
    )

    return chart


def layered_distribution_plot(x, data, hue=None, opacity=.6, bandwidth=.3,
        steps=200, stack=None, x_pad_scaler=.2, filled=True):
    """Display a layered distribution plot.

    Parameters
    ----------
    x : Collection, str
        value to calculate distribution for.
        If x is an iterable, then x will be treated as a list values
        to use for a fold transform. If x is a str, data will not be
        fold transformed
    data : pandas.DataFrame
        dataframe containing values
    hue : str, None
        value defining layers of the distribution plot. If x is a 
        a string, then hue must be specified. Otherwise legend will
        be named by the hue value.
    opacity : float
        opacity of the distribution plot layers
    bandwidth : float
        bandwidth used for density calculations
    steps : int
        number of  steps used for smoothing distribution lines
    stack : str, None, bool
        argument for stack parameter in altair. If None,
        then the areas of the layers that overlap will be
        different colors. If 'zero', then the layers will
        completly occlude one another.
    x_pad_scaler : float
        Used to extend x-axis range if needed. Adds
        x_pad_scaler * (x_max_value - x_min_value) to each
        side of the x-axis.
    filled : bool
        Whether the layers are filled or not.

    Example
    -------
    >>> import cosilico.base as base
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>> variables = ['sepal_length', 'sepal_width',
    ...             'petal_length', 'petal_width']
    >>> base.layered_distribution_plot(variables, iris)

    Returns
    -------
    altair.Chart

    """
    transformed = data.copy()
    if isinstance(x, Collection) and not isinstance(x, str):
        transformed = data.melt(value_vars=x)
        x = 'value'
        if hue is not None:
            transformed.columns = [hue if c == 'variable' else c
                    for c in transformed.columns]
        else:
            hue = 'variable'

    value_range = max(transformed[x]) - min(transformed[x])
    print(value_range)
    chart = alt.Chart(transformed).transform_density(
        density=x,
        bandwidth=bandwidth,
        groupby=[hue],
        counts=True,
        extent=[min(transformed[x]) - float(x_pad_scaler * value_range),
            max(transformed[x]) + float(x_pad_scaler * value_range)],
        steps=steps,
    ).mark_area(
        opacity=opacity,
        filled=filled,
    ).encode(
        x=alt.X(f'value:Q',
            title=x
        ),
        y=alt.Y('density:Q', stack=stack),
        color=alt.Color(f'{hue}:N')
    )

    return chart
