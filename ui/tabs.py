import gradio as gr
from ui.components import create_shared_components, create_image_analysis_column
from utils.log_utils import save_current_results, get_log_data

def create_webcam_tab():
    """Tạo tab webcam."""
    with gr.TabItem("📷 Webcam"):
        with gr.Row():
            # Cột phân tích ảnh
            _, _, _, save_button, save_status = create_image_analysis_column("webcam")
            
            # Cột thống kê
            create_stats_component = create_shared_components()
            chart, log_table = create_stats_component()
            
            # Thiết lập sự kiện lưu kết quả
            save_button.click(
                save_current_results,
                outputs=[save_status, chart]
            ).then(
                get_log_data,
                outputs=log_table
            )

def create_upload_tab():
    """Tạo tab tải ảnh lên."""
    with gr.TabItem("🖼️ Tải ảnh lên"):
        with gr.Row():
            # Cột phân tích ảnh
            _, _, _, save_button, save_status = create_image_analysis_column("upload")
            
            # Cột thống kê
            create_stats_component = create_shared_components()
            upload_chart, upload_log_table = create_stats_component()
            
            # Thiết lập sự kiện lưu kết quả
            save_button.click(
                save_current_results,
                outputs=[save_status, upload_chart]
            ).then(
                get_log_data,
                outputs=upload_log_table
            )