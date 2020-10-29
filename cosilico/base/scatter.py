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
    mark_kwargs = {
        'opacity': opacity
    }
    if color is not None and hue is None:
        mark_kwargs['color'] = color

    encode_kwargs = {}
    if hue is not None: encode_kwargs['color'] = f'{hue}:N'

    chart = alt.Chart(data).mark_point(**mark_kwargs).encode(
        x=alt.X(f'{x}:Q',
            scale=alt.Scale(zero=not x_autoscale)
        ),
        y=alt.Y(f'{y}:Q',
            scale=alt.Scale(zero=not y_autoscale)
        ),
        **encode_kwargs
    )

    return chart


def jointplot(x, y, data, hue=None, color=None, show_x=True,
        show_y=True, opacity=.6, padding_scalar=.05, maxbins=30,
        hist_height=50):
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
    opacity : float
        Opacity of the histograms in the plot
    maxbins : int
        Max bins for the histograms
    hist_height : int
        Height of histograms

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
    chart = alt.Chart(data)

    x_diff = max(data[x]) - min(data[x])
    y_diff = max(data[y]) - min(data[y])
    xscale = alt.Scale(domain=(min(data[x]) - (x_diff * padding_scalar),
        max(data[x]) + (x_diff * padding_scalar)))
    yscale = alt.Scale(domain=(min(data[y]) - (y_diff * padding_scalar),
        max(data[y]) + (y_diff * padding_scalar)))

    area_kwargs = {'opacity': opacity, 'interpolate': 'step'}

    mark_kwargs = {}
    if hue is not None:
        mark_kwargs['color'] = f'{hue}:N'

    points = chart.mark_circle().encode(
        alt.X(x, scale=xscale),
        alt.Y(y, scale=yscale),
        **mark_kwargs
    )

    encode_kwargs = {}
    if hue is not None:
        encode_kwargs['color'] = f'{hue}:N'
    top_hist = chart.mark_area(**area_kwargs).encode(
        alt.X('sepal_length:Q',
              # when using bins, the axis scale is set through
              # the bin extent, so we do not specify the scale here
              # (which would be ignored anyway)
              bin=alt.Bin(maxbins=maxbins, extent=xscale.domain),
              stack=None,
              title='',
              axis=alt.Axis(labels=False, tickOpacity=0.)
             ),
        alt.Y('count()', stack=None, title=''),
        **encode_kwargs
    ).properties(height=hist_height)
    
    right_hist = chart.mark_area(**area_kwargs).encode(
        alt.Y('sepal_width:Q',
              bin=alt.Bin(maxbins=maxbins, extent=yscale.domain),
              stack=None,
              title='',
              axis=alt.Axis(labels=False, tickOpacity=0.)
             ),
        alt.X('count()', stack=None, title=''),
        **encode_kwargs
    ).properties(width=hist_height)
    
    if top_hist and right_hist:
        return top_hist & (points | right_hist)
    if top_hist and not right_hist:
        return top_hist & points
    if not top_hist and right_hist:
        return points | right_hist
    return points

#    points = scatterplot(x, y, data, hue=hue, color=color)
#
#    if show_x:
#        bottom = base.distribution_plot(x, data, line_only=True)
#    if show_y:
#        right = base.distribution_plot(y, data, line_only=True)
#

#    points = alt.Chart(source).mark_point().encode(
#        x='Horsepower:Q',
#        y='Miles_per_Gallon:Q',
#        color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
#    ).add_selection(
#        brush
#    )
    # transform 
#    alt.Chart(data).transform_fold(
#        ['Trial A', 'Trial B', 'Trial C'],
#        as_=['Experiment', 'Measurement']
#    ).mark_area(
#        opacity=0.3,
#        interpolate='step'
#    ).encode(
#        alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
#        alt.Y('count()', stack=None),
#        alt.Color('Experiment:N')
#    ) 
#    
#    bars = alt.Chart(source).mark_bar().encode(
#        y='Origin:N',
#        color='Origin:N',
#        x='count(Origin):Q'
#    ).transform_filter(
#        brush
#    )
#    
#    points & bars
