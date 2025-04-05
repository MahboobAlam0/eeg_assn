# eeg_utils.py (Shared logic)
import numpy as np
import pandas as pd
import pywt
import mne
from scipy.signal import hilbert


def load_eeg_excel(file, sheet_name):
    df = pd.read_excel(file, sheet_name=sheet_name)
    df.drop(columns=[col for col in df.columns if "Unnamed" in col], inplace=True)
    return df


def preprocess_to_raw(df, sfreq):
    ch_names = list(df.columns[1:])  # ✅ Convert Index to list
    data = df[ch_names].T.values     # Only the EEG channels
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(data, info)
    return raw



def compute_envelope(signal):
    analytic = hilbert(signal)
    envelope = np.abs(analytic)
    return envelope


def detect_spindles(signal, sfreq, threshold_factor=2.5, min_duration=0.5):
    envelope = compute_envelope(signal)
    threshold = threshold_factor * np.std(envelope)
    above = envelope > threshold

    starts, ends = [], []
    in_spindle = False
    for i, val in enumerate(above):
        if val and not in_spindle:
            in_spindle = True
            starts.append(i)
        elif not val and in_spindle:
            in_spindle = False
            ends.append(i)

    if len(ends) < len(starts):
        ends.append(len(above)-1)

    spindles = []
    for s, e in zip(starts, ends):
        dur = (e - s) / sfreq
        if dur >= min_duration:
            spindles.append((s, e))
    return spindles


def compute_wavelet(signal, sfreq, fmin=8, fmax=13):
    scales = np.arange(1, 128)
    coef, freqs = pywt.cwt(signal, scales, 'morl', 1/sfreq)
    band_mask = (freqs >= fmin) & (freqs <= fmax)
    return coef[band_mask, :], freqs[band_mask]


def get_epochs(signal, sfreq, duration_sec=10):
    samples_per_epoch = int(duration_sec * sfreq)
    return [signal[i:i+samples_per_epoch] for i in range(0, len(signal), samples_per_epoch) if i+samples_per_epoch <= len(signal)]

