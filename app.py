import gradio as gr
from ui.tabs import create_webcam_tab, create_upload_tab
from utils.log_utils import get_log_data, create_satisfaction_chart

# --- Tạo giao diện Gradio ---
with gr.Blocks(title="Demo Phân Tích Cảm Xúc", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📊 Demo AI Phân Tích Cảm Xúc Tại Quầy Giao Dịch")
    gr.Markdown("""
    Ứng dụng này sử dụng camera hoặc ảnh tải lên để phát hiện khuôn mặt và đánh giá cảm xúc,
    từ đó suy ra mức độ hài lòng của người dân.
    """)
    
    with gr.Tabs():
        log_table,chart = create_webcam_tab()
        upload_log_table,upload_chart = create_upload_tab()
    
    # Tải dữ liệu log ban đầu khi khởi động
    demo.load(get_log_data, outputs=log_table)
    demo.load(get_log_data, outputs=upload_log_table)
    demo.load(create_satisfaction_chart, outputs=chart)
    demo.load(create_satisfaction_chart, outputs=upload_chart)

# --- Chạy ứng dụng ---
if __name__ == "__main__":
    demo.launch(share=True, debug=True)  # share=True cho phép truy cập từ xa