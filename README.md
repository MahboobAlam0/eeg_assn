# EEG Alpha Spindle Analyzer

This Streamlit web application allows for EEG alpha spindle analysis and visualization using raw EEG data stored in Excel files. It supports detection, comparison, and visualization of spindles using signal processing techniques like the Hilbert transform and Continuous Wavelet Transform.

---

## 🧠 Features

### 1. **Alpha Spindle Count Comparison**
- Detects and counts total alpha spindles (8–13 Hz) across all electrodes.
- Compares spindle counts between ECBL and EOBL sheets.

### 2. **Electrode-wise Spindle Count**
- Counts alpha spindles for each electrode individually.
- Useful for identifying spatial patterns of brain activity.

### 3. **Wavelet Transform Visualization**
- Displays a scaleogram (wavelet power spectrum) for any electrode.
- Highlights alpha band frequency activity over time.

### 4. **Epoch-based Spindle Detection**
- Divides signal into 10-second epochs.
- Visualizes spindle activity and scaleogram per epoch.
- Provides spindle counts per epoch.

---

## 🛠 Tech Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Backend Logic**: Python functions (in `eeg_utils.py`)
- **Signal Processing**:
  - [MNE-Python](https://mne.tools/stable/index.html)
  - [PyWavelets](https://pywavelets.readthedocs.io/)
  - Scipy's Hilbert transform

---

## 📁 File Structure
```
├── app.py              # Streamlit UI for the app
├── eeg_utils.py        # Core EEG processing functions (reusable)
├── README.md
└── data/
    └── Original_Data.xlsx  # EEG data file with ECBL and EOBL sheets
```

---

## 🚀 How to Run
1. Clone or download this repo.
2. Install dependencies:
```bash
pip install streamlit mne pywavelets pandas openpyxl matplotlib
```
3. Run the app:
```bash
streamlit run app.py
```

---

## 📌 Notes
- Sampling frequency is fixed at **512 Hz**.
- Spindle detection uses a threshold based on **Hilbert envelope** (threshold = `2.5 × std`).
- You can upload your own `.xlsx` file with EEG data sheets (`ECBL`, `EOBL`).
- Time column is optional — calculated from sample index if missing.

---

## 📬 Future Enhancements
- Integrate ML models for auto-labeling spindles.
- Save/export visualizations and summaries.
- Add filters for spindle duration, amplitude, and frequency range.

---

Made with ❤️ for EEG signal exploration.
