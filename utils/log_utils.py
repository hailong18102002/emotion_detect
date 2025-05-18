import os
import pandas as pd
import matplotlib.pyplot as plt
from config.constants import LOG_FILE_PATH
from utils.image_utils import get_current_results

def load_log():
    """Tải log từ file CSV nếu có."""
    if os.path.exists(LOG_FILE_PATH):
        try:
            return pd.read_csv(LOG_FILE_PATH)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["Thời gian", "Cảm xúc (gốc)", "Cảm xúc (TV)", "Đánh giá", "Biểu tượng"])
    return pd.DataFrame(columns=["Thời gian", "Cảm xúc (gốc)", "Cảm xúc (TV)", "Đánh giá", "Biểu tượng"])

def save_log_entry(log_data_list):
    """Lưu một mục log mới vào file CSV."""
    if not log_data_list:
        return "Không có dữ liệu để lưu"
        
    df_new_entries = pd.DataFrame([{
        "Thời gian": entry["timestamp"],
        "Cảm xúc (gốc)": entry["dominant_emotion_eng"],
        "Cảm xúc (TV)": entry["emotion_vn"],
        "Đánh giá": entry["satisfaction_vn"],
        "Biểu tượng": entry["satisfaction_icon"]
    } for entry in log_data_list])

    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    if not os.path.exists(LOG_FILE_PATH) or os.path.getsize(LOG_FILE_PATH) == 0:
        df_new_entries.to_csv(LOG_FILE_PATH, index=False, encoding='utf-8-sig')
    else:
        df_new_entries.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False, encoding='utf-8-sig')
    
    return f"Đã lưu {len(log_data_list)} kết quả vào {LOG_FILE_PATH}"

def create_satisfaction_chart():
    """Tạo biểu đồ thống kê mức độ hài lòng."""
    log_df = load_log()
    if log_df.empty:
        return None
    
    satisfaction_counts = log_df["Đánh giá"].value_counts()
    
    # Tạo biểu đồ bằng matplotlib
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Xác định màu dựa trên nhãn
    colors = []
    for idx in satisfaction_counts.index:
        if idx == "Hài lòng":
            colors.append('green')
        elif idx == "Bình thường":
            colors.append('yellow') 
        else:  # "Không hài lòng"
            colors.append('red')
    
    satisfaction_counts.plot(kind='bar', ax=ax, color=colors)
    plt.title('Thống kê mức độ hài lòng')
    plt.xlabel('Mức độ hài lòng')
    plt.ylabel('Số lượng')
    plt.tight_layout()
    
    return fig

def get_log_data():
    """Lấy dữ liệu log hiện tại để hiển thị trong bảng."""
    log_df = load_log()
    if log_df.empty:
        return None
    
    # Chỉ trả về 10 dòng gần nhất để hiển thị
    recent_logs = log_df.tail(10).reset_index(drop=True)
    return recent_logs

def save_current_results():
    """Lưu kết quả phân tích hiện tại vào log."""
    current_results = get_current_results()
    if not current_results:
        return "Không có kết quả nào để lưu"
    
    result = save_log_entry(current_results)
    
    # Cập nhật biểu đồ
    chart = create_satisfaction_chart()
    
    return result, chart