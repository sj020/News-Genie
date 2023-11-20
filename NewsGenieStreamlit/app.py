import streamlit as st
from Models.BART import Bart
from Models.T5 import T5

st.title('Text Summarization')

models_list = ('BART', 'T5')
model = st.selectbox('Choose the model: ', models_list)

text = st.text_area('Text Input')

def run_model(text):

    if model == 'BART':
        # Output we got after running Bart model
        output = Bart(text)

        st.write('Summary from BART')
        st.success(output[0])
    
    elif model == "T5":
        # Output we get after running T5 Model
        output = T5(text)

        st.write('Summary from T5')
        st.success(output[0])

if st.button('Submit'):
    run_model(text)
    
