"""
Real-Time Activity Prediction Visualizer
Receives predictions from Nicla Sense ME running multi_class_predict.py via UDP.
Uses the same reliable pattern as imu_data_visualizer.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import socket
import threading
from datetime import datetime
from collections import deque
from dataclasses import dataclass, field

# --- Configuration ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5007  # Must match PORT in multi_class_predict.py
MAX_HISTORY = 100  # Number of predictions to keep in history
STABILITY_WINDOW = 10  # Number of predictions for stable display (majority voting)

ACTIVITY_MAP = {
    0: "sitting",
    1: "standing",
    2: "walking",
    3: "brisk_walking",
    4: "jogging",
    5: "cycling",
    6: "stair_up",
    7: "stair_down",
    8: "sit_stand_sit",
    9: "phone_interaction",
    10: "eating_with_spoon",
    11: "pick_and_place",
}

# Activity colors for visualization
ACTIVITY_COLORS = {
    "sitting": "#4CAF50",
    "standing": "#8BC34A",
    "walking": "#2196F3",
    "brisk_walking": "#03A9F4",
    "jogging": "#FF5722",
    "cycling": "#9C27B0",
    "stair_up": "#FF9800",
    "stair_down": "#FFC107",
    "sit_stand_sit": "#00BCD4",
    "phone_interaction": "#E91E63",
    "eating_with_spoon": "#795548",
    "pick_and_place": "#607D8B",
}

# Activity emojis for display
ACTIVITY_EMOJIS = {
    "sitting": "🪑",
    "standing": "🧍",
    "walking": "🚶",
    "brisk_walking": "🚶‍♂️💨",
    "jogging": "🏃",
    "cycling": "🚴",
    "stair_up": "⬆️🪜",
    "stair_down": "⬇️🪜",
    "sit_stand_sit": "🔄",
    "phone_interaction": "📱",
    "eating_with_spoon": "🥄",
    "pick_and_place": "📦",
}

st.set_page_config(
    layout="wide", 
    page_title="Activity Prediction Visualizer",
    page_icon="🎯"
)


# ===== Shared Data Store (Thread-Safe) - Same pattern as imu_data_visualizer.py =====
@dataclass
class PredictionStore:
    """Thread-safe data store for UDP predictions."""
    buffer: deque = field(default_factory=lambda: deque(maxlen=MAX_HISTORY))
    recent_predictions: deque = field(default_factory=lambda: deque(maxlen=STABILITY_WINDOW))
    activity_counts: dict = field(default_factory=lambda: {v: 0 for v in ACTIVITY_MAP.values()})
    current_prediction: dict = field(default_factory=lambda: None)
    stable_activity: str = None
    total_count: int = 0
    is_running: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock)


@st.cache_resource
def get_data_store():
    """Singleton data store that persists across reruns."""
    return PredictionStore()


def get_majority_activity(predictions):
    """Get the most common activity from recent predictions."""
    if len(predictions) == 0:
        return None
    counts = {}
    for pred in predictions:
        activity = pred.get('activity', 'unknown')
        counts[activity] = counts.get(activity, 0) + 1
    return max(counts.keys(), key=lambda k: counts[k])


@st.cache_resource
def get_udp_thread():
    """Start persistent UDP receiver thread - same pattern as imu_data_visualizer.py."""
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
                    print(f"[PredictionReceiver] Bound to {UDP_IP}:{UDP_PORT}")
                
                try:
                    data, addr = sock.recvfrom(1024)
                    decoded = data.decode().strip()
                    parts = [p.strip() for p in decoded.split(",")]
                    
                    # Expected format: timestamp_ms, label_int, activity_str, ax, ay, az, gx, gy, gz
                    if len(parts) == 9:
                        ts_ms = int(parts[0])
                        label_int = int(parts[1])
                        activity_str = parts[2]
                        ax, ay, az = float(parts[3]), float(parts[4]), float(parts[5])
                        gx, gy, gz = float(parts[6]), float(parts[7]), float(parts[8])
                        
                        prediction = {
                            'timestamp_ms': ts_ms,
                            'label': label_int,
                            'activity': activity_str,
                            'ax': ax, 'ay': ay, 'az': az,
                            'gx': gx, 'gy': gy, 'gz': gz,
                            'received_at': datetime.now()
                        }
                        
                        with store.lock:
                            if store.is_running:
                                store.buffer.append(prediction)
                                store.recent_predictions.append(prediction)
                                store.current_prediction = prediction
                                store.stable_activity = get_majority_activity(store.recent_predictions)
                                store.total_count += 1
                                
                                if activity_str in store.activity_counts:
                                    store.activity_counts[activity_str] += 1
                                    
                except socket.timeout:
                    continue
                except ValueError:
                    continue
                    
            except Exception as e:
                print(f"[PredictionReceiver] Socket error: {e}")
                if sock:
                    try:
                        sock.close()
                    except:
                        pass
                    sock = None
                time.sleep(0.5)
        
        if sock:
            sock.close()
    
    thread = threading.Thread(target=receiver_loop, daemon=True)
    thread.start()
    return thread, stop_event


# ===== Helper Functions =====
def get_all_data():
    """Get all buffered data."""
    store = get_data_store()
    with store.lock:
        if len(store.buffer) == 0:
            return None, None, None, {}, 0, store.is_running
        return (
            list(store.buffer),
            store.current_prediction,
            store.stable_activity,
            dict(store.activity_counts),
            store.total_count,
            store.is_running
        )


def start_receiving():
    """Start receiving predictions."""
    store = get_data_store()
    with store.lock:
        store.buffer.clear()
        store.recent_predictions.clear()
        store.activity_counts = {v: 0 for v in ACTIVITY_MAP.values()}
        store.current_prediction = None
        store.stable_activity = None
        store.total_count = 0
        store.is_running = True


def stop_receiving():
    """Stop receiving predictions."""
    store = get_data_store()
    with store.lock:
        store.is_running = False


def reset_data():
    """Clear all data."""
    store = get_data_store()
    with store.lock:
        store.buffer.clear()
        store.recent_predictions.clear()
        store.activity_counts = {v: 0 for v in ACTIVITY_MAP.values()}
        store.current_prediction = None
        store.stable_activity = None
        store.total_count = 0


# ===== Initialize Background Thread =====
get_udp_thread()


# ===== UI Layout =====
st.title("🎯 Real-Time Activity Prediction Visualizer")

store = get_data_store()

with st.sidebar:
    st.header("📡 Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if not store.is_running:
            if st.button("▶️ Start", type="primary", use_container_width=True):
                start_receiving()
                st.rerun()
        else:
            if st.button("⏹️ Stop", type="secondary", use_container_width=True):
                stop_receiving()
                st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_data()
            st.rerun()
    
    st.markdown("---")
    
    # Status
    if store.is_running:
        st.markdown("### 🟢 RECEIVING")
        st.metric("Total Predictions", store.total_count)
        if store.stable_activity:
            st.metric("Stable Activity", store.stable_activity.replace('_', ' ').title())
    else:
        st.markdown("### ⏸️ IDLE")
        st.caption("Click Start to receive predictions")
    
    st.markdown("---")
    st.caption(f"UDP Port: {UDP_PORT}")
    st.caption("Ensure Nicla is running multi_class_predict.py")


# ===== Main Content =====
if store.is_running:
    st.caption(f"📡 Receiving predictions from Nicla Sense ME via UDP port {UDP_PORT}")
    
    # Create placeholders for real-time updates
    current_activity_placeholder = st.empty()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Prediction History")
        history_placeholder = st.empty()
    
    with col2:
        st.markdown("### 📈 Activity Distribution")
        distribution_placeholder = st.empty()
    
    imu_col1, imu_col2 = st.columns(2)
    with imu_col1:
        st.markdown("### 📐 Accelerometer")
        accel_placeholder = st.empty()
    with imu_col2:
        st.markdown("### 🔄 Gyroscope")
        gyro_placeholder = st.empty()
    
    status_placeholder = st.empty()
    
    # Main update loop - use timestamp for unique keys
    import time as time_module
    while store.is_running:
        unique_id = int(time_module.time() * 1000)  # Millisecond timestamp for unique keys
        history, current, stable_activity, counts, total, is_running = get_all_data()
        
        if not is_running:
            break
        
        # Current Activity Display - Use STABLE activity for display (majority voted)
        display_activity = stable_activity if stable_activity else (current.get('activity', 'unknown') if current else None)
        
        if display_activity:
            emoji = ACTIVITY_EMOJIS.get(display_activity, '❓')
            color = ACTIVITY_COLORS.get(display_activity, '#666666')
            label = list(ACTIVITY_MAP.keys())[list(ACTIVITY_MAP.values()).index(display_activity)] if display_activity in ACTIVITY_MAP.values() else "?"
            
            current_activity_placeholder.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}22 0%, {color}44 100%);
                border-left: 6px solid {color};
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            ">
                <span style="font-size: 64px;">{emoji}</span>
                <h1 style="color: {color}; margin: 10px 0; font-size: 42px;">
                    {display_activity.replace('_', ' ').upper()}
                </h1>
                <p style="font-size: 18px; color: #888;">
                    Label: {label} | Total: {total} | Stability: {STABILITY_WINDOW} samples
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            current_activity_placeholder.info("⏳ Waiting for predictions from Nicla Sense ME...")
        
        # Prediction History Timeline
        if history and len(history) > 0:
            df_history = pd.DataFrame(history)
            
            # Convert to relative time
            if 'timestamp_ms' in df_history.columns:
                start_ts = df_history['timestamp_ms'].iloc[0]
                df_history['time_s'] = (df_history['timestamp_ms'] - start_ts) / 1000.0
            else:
                df_history['time_s'] = range(len(df_history))
            
            # Create timeline chart
            fig = go.Figure()
            
            # Add activity labels as colored markers
            for activity in df_history['activity'].unique():
                mask = df_history['activity'] == activity
                activity_data = df_history[mask]
                fig.add_trace(go.Scatter(
                    x=activity_data['time_s'],
                    y=activity_data['label'],
                    mode='markers+lines',
                    name=activity.replace('_', ' ').title(),
                    marker=dict(
                        size=10,
                        color=ACTIVITY_COLORS.get(activity, '#666666'),
                    ),
                    line=dict(width=1, color=ACTIVITY_COLORS.get(activity, '#666666')),
                ))
            
            fig.update_layout(
                height=250,
                template='plotly_dark',
                xaxis_title="Time (s)",
                yaxis_title="Activity Label",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=40, b=40),
            )
            
            history_placeholder.plotly_chart(fig, key=f"hist_{unique_id}")
            
            # Activity Distribution Pie Chart
            filtered_counts = {k: v for k, v in counts.items() if v > 0}
            
            if filtered_counts:
                fig_pie = go.Figure(data=[go.Pie(
                    labels=[k.replace('_', ' ').title() for k in filtered_counts.keys()],
                    values=list(filtered_counts.values()),
                    marker_colors=[ACTIVITY_COLORS.get(k, '#666666') for k in filtered_counts.keys()],
                    hole=0.4,
                    textinfo='percent+label',
                    textposition='outside',
                )])
                
                fig_pie.update_layout(
                    height=300,
                    template='plotly_dark',
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20),
                )
                
                distribution_placeholder.plotly_chart(fig_pie, key=f"dist_{unique_id}")
            else:
                distribution_placeholder.info("Collecting data...")
            
            # IMU Data from predictions
            if 'ax' in df_history.columns:
                accel_df = df_history.set_index('time_s')[['ax', 'ay', 'az']].copy()
                accel_df.columns = ['AX', 'AY', 'AZ']
                accel_placeholder.line_chart(accel_df, height=200)
            
            if 'gx' in df_history.columns:
                gyro_df = df_history.set_index('time_s')[['gx', 'gy', 'gz']].copy()
                gyro_df.columns = ['GX', 'GY', 'GZ']
                gyro_placeholder.line_chart(gyro_df, height=200)
            
            # Status bar
            duration = df_history['time_s'].max() if 'time_s' in df_history.columns and len(df_history) > 0 else 0
            rate = len(df_history) / duration if duration > 0 else 0
            status_placeholder.success(f"🟢 Receiving — {total} predictions | {duration:.1f}s | ~{rate:.1f} pred/s")
        else:
            history_placeholder.info("⏳ Waiting for prediction history...")
            distribution_placeholder.info("⏳ Collecting distribution data...")
            accel_placeholder.info("⏳ Waiting for IMU data...")
            gyro_placeholder.info("⏳ Waiting for IMU data...")
            status_placeholder.warning(f"Waiting for UDP data on port {UDP_PORT}...")
        
        # Update interval - 500ms for smooth display
        time.sleep(0.5)
    
    # After loop ends
    current_activity_placeholder.empty()
    history_placeholder.empty()
    distribution_placeholder.empty()
    accel_placeholder.empty()
    gyro_placeholder.empty()
    status_placeholder.info("🔹 Stopped. Click **Start** to begin again.")

else:
    # Idle state
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        margin: 40px 0;
    ">
        <span style="font-size: 80px;">🎯</span>
        <h2 style="color: #e94560; margin: 20px 0;">Activity Prediction Visualizer</h2>
        <p style="font-size: 18px; color: #888; max-width: 600px; margin: 0 auto;">
            This dashboard visualizes real-time activity predictions from the Nicla Sense ME 
            running <code>multi_class_predict.py</code>. The on-chip ML model classifies 
            12 different human activities.
        </p>
        <br>
        <p style="font-size: 16px; color: #666;">
            Click <b>Start</b> in the sidebar to begin receiving predictions on port <b>{UDP_PORT}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Activity Legend
    st.markdown("### 📋 Supported Activities")
    
    cols = st.columns(4)
    for i, (key, name) in enumerate(ACTIVITY_MAP.items()):
        col = cols[i % 4]
        emoji = ACTIVITY_EMOJIS.get(name, '❓')
        color = ACTIVITY_COLORS.get(name, '#666666')
        col.markdown(f"""
        <div style="
            background: {color}22;
            border-left: 4px solid {color};
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        ">
            <span style="font-size: 24px;">{emoji}</span>
            <span style="color: {color}; font-weight: bold;">{name.replace('_', ' ').title()}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Ensure Nicla Sense ME is running `multi_class_predict.py` with PORT=5007")
