import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")

#95%
st.header("HYPOTHESIS  TESTING  alpha = 0.05")  
#all graphs we use custom css not streamlit 
theme_plotly = None 


# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#side bar
st.sidebar.image("logo1.png",caption="")

data=pd.read_csv('blood_pressure.csv')


# Calculating mean and standard deviation
control_mean = data[data['Group'] == 'Control']['BloodPressure'].mean()
treatment_mean = data[data['Group'] == 'Treatment']['BloodPressure'].mean()
control_std = data[data['Group'] == 'Control']['BloodPressure'].std()
treatment_std = data[data['Group'] == 'Treatment']['BloodPressure'].std()
n_control = len(data[data['Group'] == 'Control'])
n_treatment = len(data[data['Group'] == 'Treatment'])

# Calculating z-score
SE = np.sqrt((control_std**2 / n_control) + (treatment_std**2 / n_treatment))
z = (treatment_mean - control_mean) / SE

# Determining critical value at alpha = 0.05
critical_value = stats.norm.ppf(0.95)


import altair as alt
# Display the data in a grid layout using Altair and Streamlit
c = alt.Chart(data).mark_bar().encode(
x=alt.X('BloodPressure:Q', bin=alt.Bin(maxbins=30)),
y='count()',
color='Group:N'
).properties(
width=500,
height=300
)


# Plotting z-distribution
x = np.linspace(-3, 3, 1000)
y = stats.norm.pdf(x, 0, 1)
 
if z > critical_value:
 st.success("**✔ REJECT NULL HYPOTHESIS:** THE NEW DRUG HAS A SIGNIFICANT EFFECT ON REDUCING BLOOD PRESSURE.")


else:
    st.success("**⚠ FAIL TO REJECT NULL HYPOTHESIS:** THE NEW DRUG DOESN'T HAVE A SIGNIFICANT EFFECT ON REDUCING BLOOD PRESSURE.")

a1,a2,a3,a4,a5=st.columns(5)
a1.metric("Control Mean",control_mean)
a2.metric("Treatment Mean",treatment_mean)
a3.metric("Control Standard Deviation",control_std)
a4.metric("Treatment Standard Deviation",treatment_std)
a5.metric("Z",z)  
style_metric_cards(background_color="#FFFFFF",border_left_color="grey",border_color="grey",box_shadow="grey")

b1,b2=st.columns(2)
with b1:   
 fig, ax = plt.subplots()
 ax.plot(x, y, color='gray')  # Set the main plot color to gray
 ax.axvline(critical_value, color='red', linestyle='--', label='Critical Value')
 ax.axvline(z, color='green', linestyle='-', label='Z-score')
 ax.fill_between(x, y, where=(x >= critical_value), color='green', alpha=0.3, label='Rejection Region')
 ax.fill_between(x, y, where=(x <= -critical_value), color='green', alpha=0.3)
 ax.legend()
 ax.set_title('Z DISTRIBUTION')
 ax.set_xlabel('Z-SCORE')
 ax.set_ylabel('PROBABILITY DENSITY')
 ax.spines['top'].set_color('gray')
 ax.spines['bottom'].set_color('gray')
 ax.spines['left'].set_color('gray')
 ax.spines['right'].set_color('gray')
 # Set the gridlines
 ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
 st.pyplot(fig)  # Display matplotlib plot in Streamlit

  
with b2:
 st.altair_chart(c, use_container_width=True)   
    
    
    
    
 
    


  
 



