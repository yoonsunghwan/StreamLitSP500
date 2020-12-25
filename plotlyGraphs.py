import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Create figure with secondary y-axis
def two_y_axis_scatter(x1,y1, name_1:str, y_title1:str, x2, y2, name_2:str, title:str, y_title2:str,x_title:str):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=x1, y=y1, name=name_1),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=x2, y=y2, name=name_2, mode ='markers', marker ={'size': 5, 'opacity': 1 ,'symbol':'diamond-open'}),
        secondary_y=True,
    )
    # Add figure title
    fig.update_layout(
        title= dict(
        text= title,
        y= 0.9,
        x=0.41,
        xanchor= 'center',
        yanchor= 'top'),
        title_font_size= 22,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y= 1,
            xanchor="right",
            x=.7
        )
    )

    # Set x-axis title
    fig.update_xaxes(title_text=x_title,
                     )

    # Set y-axes titles
    fig.update_yaxes(title_text=y_title1, secondary_y=False)
    fig.update_yaxes(title_text=y_title2, secondary_y=True)

    return fig

df = pd.read_csv('institutional_holders.csv')
total_inst_holders = df.groupby('Holder')['Value'].sum()
print(total_inst_holders.loc[df[df['Symbol']=='MMM']['Holder']])
print(df[df['Symbol']=='MMM'][['Holder','Value']])

def stacked_barplot(indiv_df,total_df,stock_symbol,title,xtitle):

    total_df= total_df.loc[indiv_df['Holder']]
    trace1=go.Bar(y=total_df.index,x= total_df.values,name="Total",orientation='h')
    trace2=go.Bar(y=indiv_df['Holder'],x= indiv_df['Value'], name= 'Symbol: '+ stock_symbol,orientation='h')
    data =[trace1,trace2]
    layout = go.Layout(xaxis=dict(title=xtitle),
                       yaxis=dict(title=""),
                       barmode="stack")

    fig = go.Figure(data, layout)
    fig.update_layout(
        title=dict(
            text=title,
            y=0.9,
            x=0.41,
            xanchor='center',
            yanchor='top'),
        title_font_size=22,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=.5
        ))
    return fig