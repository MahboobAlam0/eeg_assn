# app.py (Streamlit App)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from eeg_utils import *

st.set_page_config(page_title="EEG Alpha Spindle Analyzer", layout="wide")
st.title("EEG Alpha Spindle Analyzer")

st.warning("This app accepts only .csv and .xlsx files.")

uploaded_file = st.file_uploader("Upload EEG Data (.csv or .xlsx)", type=["csv", "xlsx"])

sheet = None
raw = None

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        sheet = "CSV"
        st.success("CSV file loaded successfully!")
    elif uploaded_file.name.endswith('.xlsx'):
        excel_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
        sheet = st.selectbox("Choose Sheet", list(excel_data.keys()))
        df = excel_data[sheet]
        st.success(f"Excel file loaded. Selected sheet: {sheet}")

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())
    st.write(f"Shape: {df.shape}")

    try:
        sfreq = 512  # Hz
        raw = preprocess_to_raw(df, sfreq)
        st.success("EEG data converted to MNE Raw object successfully.")
    except Exception as e:
        st.error(f"Error in preprocessing EEG data: {e}")

if raw is not None:
    task = st.radio("Choose Task", [
        "1. Total Alpha Spindle Count",
        "2. Electrode-wise Spindle Count",
        "3. Wavelet Power Visualization",
        "4. Epoch-based Spindle Detection"
    ])

    if task == "1. Total Alpha Spindle Count":
        total_spindles = 0
        for ch in raw.ch_names:
            signal = raw.get_data(picks=ch)[0]
            spindles = detect_spindles(signal, sfreq)
            total_spindles += len(spindles)
        st.success(f"Total Alpha Spindles in {sheet}: {total_spindles}")

    elif task == "2. Electrode-wise Spindle Count":
        st.subheader("Spindle Count Per Electrode")
        for ch in raw.ch_names:
            signal = raw.get_data(picks=ch)[0]
            spindles = detect_spindles(signal, sfreq)
            st.write(f"{ch}: {len(spindles)} spindles")

    elif task == "3. Wavelet Power Visualization":
        ch = st.selectbox("Select Electrode", raw.ch_names)
        signal = raw.get_data(picks=ch)[0]
        coefs, freqs = compute_wavelet(signal, sfreq)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(np.abs(coefs), aspect='auto', extent=[0, len(signal)/sfreq, freqs[-1], freqs[0]], cmap='viridis')
        ax.set_title(f"Wavelet Power (Alpha Band) - {ch}")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_xlabel("Time (s)")
        st.pyplot(fig)

    elif task == "4. Epoch-based Spindle Detection":
        ch = st.selectbox("Choose Electrode for Epoch View", raw.ch_names)
        signal = raw.get_data(picks=ch)[0]
        epochs = get_epochs(signal, sfreq)

        for i, ep in enumerate(epochs):
            spindles = detect_spindles(ep, sfreq)
            time = np.arange(len(ep)) / sfreq

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4), sharex=True)
            ax1.plot(time, ep, label="Signal")
            ax1.set_title(f"Epoch {i+1} - Spindles: {len(spindles)}")
            for s, e in spindles:
                ax1.axvspan(s/sfreq, e/sfreq, color='red', alpha=0.3)
            ax1.legend()

            coefs, freqs = compute_wavelet(ep, sfreq)
            ax2.imshow(np.abs(coefs), aspect='auto', extent=[0, len(ep)/sfreq, freqs[-1], freqs[0]], cmap='plasma')
            ax2.set_ylabel("Freq (Hz)")
            ax2.set_xlabel("Time (s)")
            ax2.set_title("Wavelet Scaleogram")

            st.pyplot(fig)