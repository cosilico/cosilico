import altair as alt
import pandas as pd


def stripplot(x, y, data, size=8, y_autoscale=True,
        y_label=None, x_label=None,):
    """Display a basic stripplot
    
    Largely based on
    https://altair-viz.github.io/gallery/stripplot.html
    
    Parameters
    ----------
    x : str, None
        Column in data used for stripplot columns.
        If x is None or not in data, one column will be used.
    y : str
        Column in data used for stripplot y axis
    data : pandas.DataFrame
        Dataframe holding x and y
    size : int
        Size of circle markers
    y_autoscale : bool
        Autoscale the y-axis to fit the data,
        otherwise axis starts at zero.
    y_label : str, None
        Title of y-axis. If None then defaults to y.
    x_label : str, None
        Title of x-axis. If None then defaults to x.

    
    Example
    -------
    >>> import cosilico.base as base
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.stripplot('species', 'sepal_width', iris)

    Returns
    -------
    altair.Chart 
    
    .. output::
           https://static.streamlit.io/0.56.0-xTAd/index.html?id=Fdhg51uMbGMLRRxXV6ubzp
           height: 600px

    """
    if x in data.columns:
        column=alt.Column(
            f'{x}:N',
            header=alt.Header(
                labelAngle=-90,
                titleOrient='top',
                labelOrient='bottom',
                labelAlign='right',
                labelPadding=3,
            ),
        )
    else:
        column=alt.Column(
            f'{x}:N',
            header=alt.Header(
                labels=False,
                title=x,
                titleOrient='top',
            ),
        )

    stripplot =  alt.Chart(data, width=40).mark_circle(size=size).encode(
        x=alt.X(
            'jitter:Q',
            title=x_label if x_label is not None else x,
            axis=alt.Axis(values=[0],
                ticks=True if x in data.columns else False,
                grid=False, labels=False),
            scale=alt.Scale(),
        ),
        y=alt.Y(f'{y}:Q',
            title=y_label if y_label is not None else y,
            scale=alt.Scale(zero=not y_autoscale)
        ),
        color=alt.Color(f'{x}:N', legend=None),
        column=column,

    ).transform_calculate(
        # Generate Gaussian jitter with a Box-Muller transform
        jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
    )

    return stripplot
