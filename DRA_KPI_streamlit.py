import streamlit as st
import pandas as pd
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import gridplot
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.models.tools import HoverTool
from bokeh.models import ColumnDataSource


##Preview web title
st.title('VDRA KPI')

##Read csv file
df=pd.read_csv('https://github.com/ekng93/streamlit_v1.0/blob/main/sample_data.csv', index_col=0)

##Extract data and time
df['date_time']=pd.to_datetime(df['date_time'])
temp=[]
temp1=[]
for d in df['date_time']:
	temp.append(d.date())
	temp1.append(d.time())
df['date']=temp
df['time']=temp1

##sidebar header
st.sidebar.header('User Input Features')

##select node
node=sorted( df['NE'].unique() )
selected_node=st.sidebar.selectbox('Node', node)
#print (selected_node)
df2=df.loc[df['NE']==selected_node]

#node=sorted( df['NE'].unique() )
#selected_node=st.sidebar.multiselect('Node', node, node)
#print (selected_node)
#df2=df[ (df['NE'].isin(selected_node)) ]


##select date
date=sorted(df2['date'].tail(200).unique())
selected_date=st.sidebar.multiselect('Date', date, date)
#print (selected_date)
df3=df2[ (df2['date'].isin(selected_date)) ]

##select feature
df3.set_index('date_time', inplace=True)
df_temp=df3.drop(columns=['NE', 'date', 'time'])
features=sorted(df_temp.columns)
selected_features=st.sidebar.selectbox('Type of KPI', features)
df4=df3.loc[:,('date','time','NE', selected_features)]


##preview the dataframe with selected condition
st.write('Data Dimension: ' + str(df4.shape[0]) + ' rows and ' + str(df4.shape[1]) + ' columns.')
st.dataframe(df4)


#Identify how many days and which position start change date for slicing later
c=df4['date'].values
temp=[]
x=len(df4)

#Identify how many days and which position start change date for slicing later
for i in range (0,x-1):
    if c[i]!=c[i+1] and i<(x-1):
        temp.append(i+1)
    
    else:
        pass

#How many days identified and which position start change date for slicing later
u=len(temp) + 1 #how many days

#show values
#print (u) 
#print (temp[0])

s=[]
s=temp #position start change date

#show values
#print (s[0])
print (u)
print (s)

##Choose the visualization based on number of u
if u==1:
   df5 = df4.iloc[0:len(df4)-1,:]
  
   df5.set_index('time',inplace=True)

   source1 = ColumnDataSource(data={
   'date'  : df5['date'],
   'time'	 : df5.index,
   'count' : df5[selected_features].values
   })

   colour=['#ff7f0e','#2ca02c','#d62728','#1f77b4']
   #output_file("test1.html")
   p = figure(x_axis_label='Time', y_axis_label=selected_features,x_axis_type='datetime',title=selected_node, plot_width=700, plot_height=400)
   p.line('time','count',source=source1,line_width=4, color=str(colour[0]),legend_label=str(df5.iloc[1,0]))


elif u==2:
   df5 = df4.iloc[(slice(0,s[0]-1)),:]
   df6 = df4.iloc[(slice(s[0],len(df4)-1)),:]

   df5.set_index('time',inplace=True)

   df6.set_index('time',inplace=True)


   source1 = ColumnDataSource(data={
   'date'  : df5['date'],
   'time'	 : df5.index,
   'count' : df5[selected_features].values
   })
   
   source2 = ColumnDataSource(data={
   'date'  : df6['date'],
   'time'	 : df6.index,
   'count' : df6[selected_features].values
   })

   colour=['#ff7f0e','#2ca02c','#d62728','#1f77b4']
   #output_file("test1.html")
   p = figure(x_axis_label='Time', y_axis_label=selected_features,x_axis_type='datetime',title=selected_node, plot_width=700, plot_height=400)
   p.line('time','count',source=source1,line_width=2, color=str(colour[0]),legend_label=str(df5.iloc[1,0]))
   p.line('time','count',source=source2,line_width=4, color=str(colour[1]),legend_label=str(df6.iloc[1,0]))

elif u==3:
   df5 = df4.iloc[0:s[0]-1,:]
   df6 = df4.iloc[s[0]:s[1]-1,:]
   df7 = df4.iloc[s[1]:len(df4)-1,:]

   df5.set_index('time',inplace=True)

   df6.set_index('time',inplace=True)
   
   df7.set_index('time',inplace=True)


   source1 = ColumnDataSource(data={
   'date'  : df5['date'],
   'time'	 : df5.index,
   'count' : df5[selected_features].values
   })
   
   source2 = ColumnDataSource(data={
   'date'  : df6['date'],
   'time'	 : df6.index,
   'count' : df6[selected_features].values
   })

   source3 = ColumnDataSource(data={
   'date'  : df7['date'],
   'time'	 : df7.index,
   'count' : df7[selected_features].values
   })
   
   colour=['#ff7f0e','#2ca02c','#d62728','#1f77b4']
   #output_file("test1.html")
   p = figure(x_axis_label='Time', y_axis_label=selected_features,x_axis_type='datetime',title=selected_node, plot_width=700, plot_height=400)
   p.line('time','count',source=source1,line_width=2, color=str(colour[0]),legend_label=str(df5.iloc[1,0]))
   p.line('time','count',source=source2,line_width=2, color=str(colour[1]),legend_label=str(df6.iloc[1,0]))
   p.line('time','count',source=source3,line_width=4, color=str(colour[2]),legend_label=str(df7.iloc[1,0]))

else:
   pass

p.legend.click_policy="hide"

# add a hover tool and show the date in date time format
hover = HoverTool(mode='mouse')
hover.tooltips=[
    ('Date', '@date{%F}'),
    ('Time', '@time{%H:%M}'),
    ('Count', '@count'),
    #('(x,y)', '($x, $y)')
]
hover.formatters = {'@date': 'datetime','@time': 'datetime'}
p.add_tools(hover)


##show the chart
st.write('Chart:')
st.write(selected_features, 'of', selected_node)

st.bokeh_chart(p)
st.button("Re-run")