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
    """Display a scatterplot with axes histograms.

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
        alt.X(f'{x}:Q',
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
        alt.Y(f'{y}:Q',
              bin=alt.Bin(maxbins=maxbins, extent=yscale.domain),
              stack=None,
              title='',
              axis=alt.Axis(labels=False, tickOpacity=0.)
             ),
        alt.X('count()', stack=None, title=''),
        **encode_kwargs
    ).properties(width=hist_height)
    
    if show_x and show_y:
        return top_hist & (points | right_hist)
    if show_x and not show_y:
        return top_hist & points
    if not show_x and show_y:
        return points | right_hist
    return points


def clean_jointplot(x, y, data, hue=None, show_x=True,
        show_y=True, opacity=.6, padding_scalar=.2, bandwidth_scalar=10,
        line_height=50, top_spacing=-40, right_spacing=0,
        apply_configure_view=True):
    """Display a clean scatterplot with axes distribution lines.

    Parameters
    ----------
    x : str
        Column in data to be used for x-axis
    y : str
        Column in data to be used for y-axis
    data : pandas.DataFrame
        Dataframe holding x and y
    hue : str, None
        Column in data used to coloring the points 
    show_X : bool
        Show the line distribution for the x-axis values
    show_y : bool
        Show the line distribution for the y-axis values
    opacity : float
        Opacity of the histograms in the plot
    bandwidth_scalar : float, int
        Sets bandwidth for the density estimation.
        Bandwidth = value_range / bandwidth_scalar
    line_height : int
        Height of the distribution lines
    top_spacing : int
        Amount of spacing between top distribution line and scatter
    right_spacing : int
        Amount of spacing between right distribution line and scatter
    apply_configure_view : bool
        Whether to apply strokeWidth=0 to the configure view function.
        Note that if this is applied you cant later combine this chart
        with another chart. To combine this chart with another chart
        you will need to set apply_configure_view to False and then reapply
        .configure_view in the combined chart to make the weird axis
        borders go away

    Example
    -------
    >>> import cosilico.base as base
    >>>
    >>> import seaborn as sns
    >>> iris = sns.load_dataset('iris')
    >>>
    >>> base.clean_jointplot('sepal_length', 'sepal_width', iris, hue='species')
    
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

    transform_kwargs = {}
    if hue is not None:
        transform_kwargs['groupby'] = [hue]

    line_axis_kwargs = {'labels': False, 'tickOpacity': 0., 'domain': False,
        'grid': False}

    top_line = chart.transform_density(
        density=x,
        bandwidth=x_diff / bandwidth_scalar,
        counts=True,
        extent=xscale.domain,
        steps=200,
        **transform_kwargs
    ).mark_line(
        opacity=opacity
    ).encode(
        x=alt.X(f'value:Q',
            scale=xscale,
            title='',
            axis=alt.Axis(**line_axis_kwargs)
        ),
        y=alt.Y('density:Q',
            title='',
            axis=alt.Axis(**line_axis_kwargs)
        ),
        **encode_kwargs
    ).properties(height=line_height)

    right_line = chart.transform_density(
        density=y,
        bandwidth=y_diff / bandwidth_scalar,
        counts=True,
        extent=yscale.domain,
        steps=200,
        **transform_kwargs
    ).mark_line(
        opacity=opacity
    ).encode(
        y=alt.X(f'value:Q',
            scale=yscale,
            title='',
            axis=alt.Axis(**line_axis_kwargs)
        ),
        x=alt.Y('density:Q',
            title='',
            axis=alt.Axis(**line_axis_kwargs)
        ),
        order='value:Q',
        **encode_kwargs
    ).properties(width=line_height)

    if show_x and show_y:
        combined = alt.vconcat(top_line,
            alt.hconcat(points, right_line, spacing=right_spacing),
            spacing=top_spacing)
    if show_x and not show_y:
        combined = alt.vconcat(top_line, points, spacing=top_spacing)
    if not show_x and show_y:
        combined = alt.hconcat(points, right_line, spacing=right_spacing)
    if not show_x and not show_y:
        combined = points

    if apply_configure_view:
        combined = combined.configure_view(strokeWidth=0)

    return combined
