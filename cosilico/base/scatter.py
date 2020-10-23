import altair as alt
import pandas as pd


def scatterplot(x, y, data, hue=None, color=None, opacity=1.,
        x_autoscale=True, y_autoscale=True):
    """Display a basic scatterplot.

    Parameters
    ----------
    x : str
        Column in data to be used for x-axis
    y : str
        Column in data to be used for y-axis
    data : pandas.DataFrame
        Dataframe holding x and y
    hue : str, None
        Column in data used to color the points
    color : str, None
        What color to display the points as
        If hue is not None, then color will be overriden by hue
    opacity : float
        Opacity of the points in the plot
    x_autoscale : bool
        Scale the x-axis to fit the data,
        otherwise axis starts at zero
    y_autoscale : bool
        Scale the y-axis to fit the data,
        otherwise axis starts at zero


    Example
    -------
    >>> import cosilico.base as base
    >>> import seaborn as sns
    >>>
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.scatterplot('sepal_length', 'sepal_width', iris, hue='species')
    
    Returns
    -------
    altair.Chart

    .. output::
           https://static.streamlit.io/0.56.0-xTAd/index.html?id=Fdhg51uMbGMLRRxXV6ubzp
           height: 600px

    """
    configure_mark_kwargs = {
        'opacity': opacity
    }
    if color is not None and hue is None:
        configure_mark_kwargs['color'] = color

    chart = alt.Chart(data).mark_point().encode(
        x=alt.X(f'{x}:Q',
            scale=alt.Scale(zero=not x_autoscale)
        ),
        y=alt.Y(f'{y}:Q',
            scale=alt.Scale(zero=not y_autoscale)
        )
    ).configure_mark(**configure_mark_kwargs)

    return chart


def jointplot(x, y, data, hue=None, color=None, show_x=True,
        show_y=True, x_autoscale=True, y_autoscale=True, opacity=1.):
    """Display a scatterplot with axes distributions.

    Parameters
    ----------
    x : str
        Column in data to be used for x-axis
    y : str
        Column in data to be used for y-axis
    data : pandas.DataFrame
        Dataframe holding x and y
    hue : str, None
        Column in data used to color the points
    color : str, None
        What color to display the points as
        If hue is not None, then color will be overriden by hue
    show_X : bool
        Show the distribution for the x-axis values
    show_y : bool
        Show the distribution for the y-axis values
    x_autoscale : bool
        Scale the x-axis to fit the data,
        otherwise axis starts at zero
    y_autoscale : bool
        Scale the y-axis to fit the data,
        otherwise axis starts at zero
    opacity : float
        Opacity of the points in the plot


    Example
    -------
    >>> import cosilico.base as base
    >>>
    >>> import seaborn as sns
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.jointplot('sepal_length', 'sepal_width', iris, hue='species')
    
    Returns
    -------
    altair.Chart

    .. output::
           https://static.streamlit.io/0.56.0-xTAd/index.html?id=Fdhg51uMbGMLRRxXV6ubzp
           height: 600px

    """
    points = scatterplot(x, y, data, hue=hue, color=color)
#    points = alt.Chart(source).mark_point().encode(
#        x='Horsepower:Q',
#        y='Miles_per_Gallon:Q',
#        color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
#    ).add_selection(
#        brush
#    )
    # transform 
    alt.Chart(data).transform_fold(
        ['Trial A', 'Trial B', 'Trial C'],
        as_=['Experiment', 'Measurement']
    ).mark_area(
        opacity=0.3,
        interpolate='step'
    ).encode(
        alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
        alt.Y('count()', stack=None),
        alt.Color('Experiment:N')
    ) 
    
    bars = alt.Chart(source).mark_bar().encode(
        y='Origin:N',
        color='Origin:N',
        x='count(Origin):Q'
    ).transform_filter(
        brush
    )
    
    points & bars
