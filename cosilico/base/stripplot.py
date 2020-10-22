import altair as alt
import pandas as pd


def stripplot(x, y, data, size=8):
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
        
    
    Example
    -------
    >>> from cosilico.base.stripplot import stripplot
    >>> import seaborn as sns
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> stripplot('species', 'sepal_width', iris)

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
            title=None,
            axis=alt.Axis(values=[0],
                ticks=True if x in data.columns else False,
                grid=False, labels=False),
            scale=alt.Scale(),
        ),
        y=alt.Y(f'{y}:Q'),
        color=alt.Color(f'{x}:N', legend=None),
        column=column,
    ).transform_calculate(
        # Generate Gaussian jitter with a Box-Muller transform
        jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )

    return stripplot
