import os
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_training_logs(base_dir="./SVYKHOA_Chatbox", file_name="trainer_state.json",
                       html_out="./training_plot.html"):
    """
    Plot training metrics from latest checkpoint and update a single HTML dashboard.
    - Không mở nhiều tab khi gọi nhiều lần
    - Chỉ cần mở training_plot.html 1 lần → nhấn F5 để xem update
    """

    # === Tìm checkpoint mới nhất ===
    checkpoint_dir = None
    max_step = -1

    for folder in os.listdir(base_dir):
        if folder.startswith("checkpoint"):
            try:
                step = int(folder.split("-")[-1])
                if step > max_step:
                    max_step = step
                    checkpoint_dir = os.path.join(base_dir, folder)
            except:
                continue

    if checkpoint_dir is None:
        print(f"Không tìm thấy checkpoint trong {base_dir}")
        return

    json_path = os.path.join(checkpoint_dir, file_name)

    if not os.path.exists(json_path):
        print("Không tìm thấy trainer_state.json trong checkpoint")
        return

    print(f"Update biểu đồ từ: {json_path}")

    # === Đọc log JSON ===
    with open(json_path, "r") as f:
        data = json.load(f)

    log_history = pd.DataFrame(data["log_history"])

    # === Tạo biểu đồ ===
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        subplot_titles=["Training Loss", "Gradient Norm", "Learning Rate"],
        vertical_spacing=0.07
    )

    fig.add_trace(go.Scatter(x=log_history["step"], y=log_history["loss"],
                             mode="lines", name="Loss"), row=1, col=1)

    fig.add_trace(go.Scatter(x=log_history["step"], y=log_history["grad_norm"],
                             mode="lines", name="Grad Norm"), row=2, col=1)

    fig.add_trace(go.Scatter(x=log_history["step"], y=log_history["learning_rate"],
                             mode="lines", name="Learning Rate"), row=3, col=1)

    fig.update_layout(
        height=900,
        width=1400,
        hovermode="x unified",
        title="Training Metrics Viewer (Auto Update)"
    )

    # === Ghi đè file HTML ===
    fig.write_html(html_out, auto_open=False)
    print(f"Biểu đồ đã cập nhật trong: {html_out}")
