"""
Real-Time IMU Data Visualizer - Flicker-Free Version
Uses st.line_chart with st.empty() for stable updates without reloading.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import glob
import time
import re
import socket
import csv
import threading
from datetime import datetime
from collections import deque
from dataclasses import dataclass, field

# --- Configuration ---
DATA_DIR = "./imu_data"
UDP_IP = "0.0.0.0"
UDP_PORT = 5006
MAX_POINTS = 500  # Display buffer
ACTIVITIES = [
    "sitting", "standing", "walking", "brisk_walking", "jogging",
    "cycling", "stair_up", "stair_down", "sit_stand_sit",
    "phone_interaction", "eating_with_spoon", "pick_and_place"
]

os.makedirs(DATA_DIR, exist_ok=True)
st.set_page_config(layout="wide", page_title="IMU Data Recorder & Visualizer")


# ===== Shared Data Store (Thread-Safe) =====
@dataclass
class DataStore:
    """Thread-safe data store for UDP samples."""
    buffer: deque = field(default_factory=lambda: deque(maxlen=MAX_POINTS))
    sample_count: int = 0
    is_running: bool = False
    is_recording: bool = False
    activity: str = "unknown"
    filepath: str = ""
    lock: threading.Lock = field(default_factory=threading.Lock)
    csv_file: object = None
    csv_writer: object = None


@st.cache_resource
def get_data_store():
    """Singleton data store that persists across reruns."""
    return DataStore()


@st.cache_resource
def get_udp_thread():
    """Start persistent UDP receiver thread."""
    store = get_data_store()
    stop_event = threading.Event()
    
    def receiver_loop():
        sock = None
        while not stop_event.is_set():
            try:
                if sock is None:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((UDP_IP, UDP_PORT))
                    sock.settimeout(0.1)
                
                try:
                    data, addr = sock.recvfrom(1024)
                    decoded = data.decode().strip()
                    parts = [p.strip() for p in decoded.split(",")]
                    
                    if len(parts) == 7:
                        ts = int(parts[0])
                        ax, ay, az = float(parts[1]), float(parts[2]), float(parts[3])
                        gx, gy, gz = float(parts[4]), float(parts[5]), float(parts[6])
                        
                        sample = {
                            'timestamp_ms': ts,
                            'ax': ax, 'ay': ay, 'az': az,
                            'gx': gx, 'gy': gy, 'gz': gz
                        }
                        
                        with store.lock:
                            if store.is_running:
                                store.buffer.append(sample)
                                store.sample_count += 1
                                
                                if store.is_recording and store.csv_writer:
                                    store.csv_writer.writerow([
                                        ts, ax, ay, az, gx, gy, gz, store.activity
                                    ])
                                    store.csv_file.flush()
                                    
                except socket.timeout:
                    continue
                except ValueError:
                    continue
                    
            except Exception as e:
                if sock:
                    sock.close()
                    sock = None
                time.sleep(0.5)
        
        if sock:
            sock.close()

    thread = threading.Thread(target=receiver_loop, daemon=True)
    thread.start()
    return thread, stop_event


# ===== Helper Functions =====
def get_csv_files():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    def extract_time(f):
        match = re.search(r'(\d{8}_\d{6})', os.path.basename(f))
        return match.group(1) if match else ""
    return sorted(csv_files, key=lambda f: extract_time(f), reverse=True)


def get_all_data():
    """Get all buffered data."""
    store = get_data_store()
    with store.lock:
        if len(store.buffer) == 0:
            return None, 0, store.is_running, store.is_recording, store.activity
        return list(store.buffer), store.sample_count, store.is_running, store.is_recording, store.activity


def start_streaming():
    store = get_data_store()
    with store.lock:
        store.buffer.clear()
        store.sample_count = 0
        store.is_running = True
        store.is_recording = False


def stop_streaming():
    store = get_data_store()
    with store.lock:
        store.is_running = False
        store.is_recording = False
        if store.csv_file:
            store.csv_file.close()
            store.csv_file = None
            store.csv_writer = None


def start_recording(activity):
    store = get_data_store()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{activity}_{timestamp}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    csv_file = open(filepath, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["timestamp_ms", "ax", "ay", "az", "gx", "gy", "gz", "activity"])

    with store.lock:
        store.buffer.clear()
        store.sample_count = 0
        store.is_running = True
        store.is_recording = True
        store.activity = activity
        store.filepath = filepath
        store.csv_file = csv_file
        store.csv_writer = csv_writer

    return filepath


def stop_recording():
    store = get_data_store()
    with store.lock:
        filepath = store.filepath
        count = store.sample_count
        store.is_running = False
        store.is_recording = False
        if store.csv_file:
            store.csv_file.close()
            store.csv_file = None
            store.csv_writer = None
    return filepath, count


# ===== Initialize Background Thread =====
get_udp_thread()


# ===== Session State =====
if 'mode' not in st.session_state:
    st.session_state.mode = 'live'
if 'selected_activity' not in st.session_state:
    st.session_state.selected_activity = 'sitting'


# ===== UI Layout =====
st.title("🎯 IMU Data Recorder & Visualizer")

with st.sidebar:
    st.header("📡 Mode")
    mode = st.radio("Mode", ["🔴 Live", "📂 Playback"], horizontal=True,
                    index=0 if st.session_state.mode == 'live' else 1,
                    label_visibility="collapsed")
    st.session_state.mode = 'live' if "Live" in mode else 'playback'
    st.markdown("---")

    if st.session_state.mode == 'live':
        st.subheader("🎬 Controls")
        
        store = get_data_store()
        
        activity = st.selectbox(
            "Activity", options=ACTIVITIES,
            index=ACTIVITIES.index(st.session_state.selected_activity),
            disabled=store.is_recording
        )
        st.session_state.selected_activity = activity
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not store.is_recording:
                if st.button("🔴 Record", type="primary", use_container_width=True):
                    start_recording(activity)
                    st.rerun()
            else:
                if st.button("⏹️ Stop Rec", type="secondary", use_container_width=True):
                    filepath, count = stop_recording()
                    st.toast(f"✅ Saved {count} samples to {os.path.basename(filepath)}")
                    st.rerun()
        
        with col2:
            if not store.is_running:
                if st.button("👁️ Stream", use_container_width=True):
                    start_streaming()
                    st.rerun()
            elif not store.is_recording:
                if st.button("⏸️ Stop", use_container_width=True):
                    stop_streaming()
                    st.rerun()
        
        st.markdown("---")
        
        # Status in sidebar
        if store.is_recording:
            st.markdown("### 🔴 RECORDING")
            st.metric("Samples", store.sample_count)
            if store.filepath:
                st.caption(f"📁 {os.path.basename(store.filepath)}")
        elif store.is_running:
            st.markdown("### 👁️ STREAMING")
            st.metric("Samples", store.sample_count)
        else:
            st.markdown("### ⏸️ IDLE")
            st.caption("Click Record or Stream")
        
        st.markdown("---")
        st.caption(f"UDP: {UDP_IP}:{UDP_PORT}")
        
    else:
        st.subheader("📂 Files")
        csv_files = get_csv_files()
        if csv_files:
            selected_file = st.selectbox(
                "File", options=csv_files,
                format_func=lambda x: os.path.basename(x)
            )
            st.session_state.playback_file = selected_file
            
            if selected_file:
                try:
                    df = pd.read_csv(selected_file)
                    st.metric("Samples", len(df))
                    if 'timestamp_ms' in df.columns:
                        duration = (df['timestamp_ms'].max() - df['timestamp_ms'].min()) / 1000
                        st.metric("Duration", f"{duration:.1f}s")
                except:
                    pass
        else:
            st.warning("No files found")


# ===== Main Content =====
if st.session_state.mode == 'live':
    store = get_data_store()
    
    if store.is_running:
        # Create FIXED placeholders that persist
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Accelerometer (g)")
            accel_placeholder = st.empty()
        
        with col2:
            st.markdown("### 🔄 Gyroscope (dps)")
            gyro_placeholder = st.empty()
        
        status_placeholder = st.empty()
        
        # Main update loop - updates placeholders IN PLACE
        while store.is_running:
            data, count, is_running, is_recording, activity = get_all_data()
            
            if not is_running:
                break
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                
                # Calculate relative time
                start_ts = df['timestamp_ms'].iloc[0]
                df['time'] = (df['timestamp_ms'] - start_ts) / 1000.0
                df = df.set_index('time')
                
                # Accelerometer chart
                accel_df = df[['ax', 'ay', 'az']].copy()
                accel_df.columns = ['AX', 'AY', 'AZ']
                accel_placeholder.line_chart(accel_df, height=350, use_container_width=True)
                
                # Gyroscope chart
                gyro_df = df[['gx', 'gy', 'gz']].copy()
                gyro_df.columns = ['GX', 'GY', 'GZ']
                gyro_placeholder.line_chart(gyro_df, height=350, use_container_width=True)
                
                # Status bar
                activity_display = activity.replace('_', ' ').title() if activity else "Live"
                duration = df.index.max() if len(df) > 0 else 0
                rate = len(df) / duration if duration > 0 else 0
                
                if is_recording:
                    status_placeholder.success(f"🔴 **Recording {activity_display}** — {count} samples | {duration:.1f}s | ~{rate:.0f} Hz")
                else:
                    status_placeholder.info(f"👁️ **Streaming** — {count} samples | {duration:.1f}s | ~{rate:.0f} Hz")
            else:
                accel_placeholder.info("⏳ Waiting for accelerometer data...")
                gyro_placeholder.info("⏳ Waiting for gyroscope data...")
                status_placeholder.warning("Waiting for UDP data on port 5006...")
            
            # Update interval - 500ms for smoother display
            time.sleep(0.5)
        
        # After loop ends
        accel_placeholder.empty()
        gyro_placeholder.empty()
        status_placeholder.info("🔹 Streaming stopped. Click **Record** or **Stream** to start again.")
        
    else:
        st.info("🔹 Click **Record** or **Stream** to start viewing live data.")
        st.caption("Ensure Nicla Sense ME is connected and running main.py with PORT=5006")

else:
    # Playback mode - Plotly with dark theme
    if hasattr(st.session_state, 'playback_file') and st.session_state.playback_file:
        try:
            df = pd.read_csv(st.session_state.playback_file)
            if 'timestamp_ms' in df.columns:
                df['time_s'] = (df['timestamp_ms'] - df['timestamp_ms'].iloc[0]) / 1000.0
            else:
                df['time_s'] = range(len(df))
            
            basename = os.path.basename(st.session_state.playback_file)
            act_match = re.match(r'^([a-z_]+)_\d{8}', basename)
            activity = act_match.group(1).replace('_', ' ').title() if act_match else "Unknown"
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure()
                for c, clr in [('ax', '#FF6B6B'), ('ay', '#4ECDC4'), ('az', '#45B7D1')]:
                    if c in df.columns:
                        fig.add_trace(go.Scattergl(
                            x=df['time_s'], y=df[c], 
                            mode='lines', name=c.upper(), 
                            line=dict(color=clr, width=1.5)
                        ))
                fig.update_layout(
                    title=f"Accelerometer — {activity}",
                    xaxis_title="Time (s)", 
                    yaxis_title="Acceleration (g)",
                    height=400,
                    template='plotly_dark',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure()
                for c, clr in [('gx', '#FF6B6B'), ('gy', '#4ECDC4'), ('gz', '#45B7D1')]:
                    if c in df.columns:
                        fig.add_trace(go.Scattergl(
                            x=df['time_s'], y=df[c], 
                            mode='lines', name=c.upper(), 
                            line=dict(color=clr, width=1.5)
                        ))
                fig.update_layout(
                    title=f"Gyroscope — {activity}",
                    xaxis_title="Time (s)", 
                    yaxis_title="Angular Rate (dps)",
                    height=400,
                    template='plotly_dark',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"📂 {basename} | {len(df)} samples | Duration: {df['time_s'].max():.1f}s")
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("🔹 Select a file from sidebar")
