import streamlit as st
import pandas as pd
import plotly.express as px
 


st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")

st.success("### ⏱ FREQUENCY  DISTRIBUTION  TABLE")

theme_plotly = None 

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#side bar
st.sidebar.image("logo1.png",caption="")

#load data
df=pd.read_csv('sales.csv')

# Calculate frequency
frequency = df['UnitPrice'].value_counts().sort_index()

# Calculate percentage frequency
percentage_frequency = frequency / len(df['UnitPrice']) * 100

# Calculate cumulative frequency
cumulative_frequency = frequency.cumsum()

# Calculate relative frequency
relative_frequency = frequency / len(df['UnitPrice'])

# Calculate cumulative relative frequency
cumulative_relative_frequency = relative_frequency.cumsum()

# Create a summary table
summary_table = pd.DataFrame({
    'Frequency': frequency,
    'Percentage Frequency': percentage_frequency,
    'Cumulative Frequency': cumulative_frequency,
    'Relative Frequency': relative_frequency,
    'Cumulative Relative Frequency': cumulative_relative_frequency
})
# Display the summary table
showData=st.multiselect('',summary_table.columns,default=["Frequency","Percentage Frequency","Cumulative Frequency","Relative Frequency","Cumulative Relative Frequency",])
st.dataframe(summary_table[showData],use_container_width=True)
 

valid_age_values = df['UnitPrice'].dropna().values

# Add legend and distribution line for mean age
mean_age = valid_age_values.mean()

# Plotting the histogram using Plotly and Streamlit
fig = px.histogram(df['UnitPrice'], y=df['UnitPrice'], nbins=10, labels={'UnitPrice': 'UnitPrice', 'count': 'Frequency'}, orientation='h')

# Add a dashed line for mean and customize its appearance
fig.add_hline(y=mean_age, line_dash="dash", line_color="red", annotation_text=f"Mean UnitPrice: {mean_age:.2f}", annotation_position="bottom right")

# Customize marker and line for bars
fig.update_traces(marker=dict(color='#51718E', line=dict(color='rgba(33, 150, 243, 1)', width=0.5)), showlegend=True, name='UnitPrice')

# Update layout for a materialized look, add gridlines, and adjust legend
fig.update_layout(
    title='UNIT PRICE DISTRIBUTION',
    yaxis_title='UnitPrice',
    xaxis_title='Frequency',
    bargap=0.1,
    legend=dict(title='Data', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    xaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)'),
    yaxis=dict(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)')
)

# Display the histogram using Streamlit
st.success("**DISTRIBUTION GRAPH**")
st.plotly_chart(fig, use_container_width=True)


 