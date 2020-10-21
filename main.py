from seminario_transf_fourier import my_fft, wt
import streamlit as st
import matplotlib.pyplot as plt
import os
import pywt

st.sidebar.header('Seminario de Matemética Numérica')
st.sidebar.subheader('Titulo: Transformada de fourier y su aplicacion en la deteccion del rango vocal')
st.write('Con este trabajo se muestra la implementación de un \
    detector de rangos vocales a través del uso de la Transformada de Fourier')
st.write('Los rangos vocales estan distribuidos de la siguiente forma (de menor a mayor):')
st.write('bajo -> baritono -> tenor -> contralto -> mezzo -> soprano')


audio_type = st.sidebar.selectbox('Tipo de audio', ('Cantante', 'Voces de personas'))
show_spectro = st.sidebar.selectbox('Mostrar espectro de Fourier', ('No', 'Si'))
audio = ''
cantate = ''

if audio_type == 'Cantante':
    cantantes = st.selectbox('Seleccione el cantante de su preferencia', ('Avriel Kaplan', 'Mitch Grassi', 'Ariana Grande'))
    audio_file = open('cantantes/' + cantantes + '.wav', 'rb')
else:
    audio = st.selectbox('Seleccionar audio a analizar', ('voz1', 'voz2', 'voz3'))
    audio_file = open('voces/' + audio + '.wav', 'rb')

audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/wav')

analizar = st.button('Analizar')


if analizar:
    if audio_type == 'Cantante':
        try:
            value, fourier_parameters, frequency = my_fft(os.getcwd() + '/cantantes', cantantes + '.wav')
            item = wt(os.getcwd() + '/cantantes', cantantes + '.wav')
            st.subheader('Fourier:    ' + value)
            st.subheader('Wavelet:    ' + item)

        except: pass
            
    else:
        try:
            value, fourier_parameters, frequency = my_fft(os.getcwd() + '/voces', audio + '.wav')
            item = wt(os.getcwd() + '/voces', audio + '.wav')
            st.subheader('Fourier:    ' + value)
            st.subheader('Wavelet:    ' + item)
        except: pass 

    if show_spectro == 'Si':
        st.header('Espectro de frecuencias de Fourier:')
        plt.plot(frequency, fourier_parameters)
        st.pyplot()
    
