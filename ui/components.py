import gradio as gr
from utils.image_utils import process_image
from utils.log_utils import save_current_results, get_log_data, create_satisfaction_chart

def create_shared_components():
    """Tạo các thành phần dùng chung cho cả 2 tab."""
    
    def create_stats_column():
        """Tạo cột thống kê."""
        with gr.Column(scale=1):
            gr.Markdown("### 📈 Thống kê và Ghi nhận")
            chart = gr.Plot(label="Thống kê mức độ hài lòng", elem_id="chart")
            log_table = gr.DataFrame(label="Lịch sử ghi nhận (10 mục gần nhất)", elem_id="log_table")
            refresh_button = gr.Button("Làm mới dữ liệu")
            
            # Thiết lập sự kiện làm mới
            refresh_button.click(
                get_log_data,
                outputs=log_table
            ).then(
                create_satisfaction_chart,
                outputs=chart
            )
            
            return chart, log_table
    
    return create_stats_column

def create_image_analysis_column(input_source_name):
    """Tạo cột phân tích ảnh."""
    with gr.Column(scale=2):
        # Input
        if input_source_name == "webcam":
            image_input = gr.Image(sources="webcam", label="Webcam", elem_id=f"{input_source_name}_input")
            analyze_button = gr.Button("Phân tích ảnh từ webcam")
        else:  # upload
            image_input = gr.Image(label="Tải ảnh lên", type="pil", elem_id=f"{input_source_name}_input")
            analyze_button = gr.Button("Phân tích ảnh đã tải lên")
        
        # Output
        image_output = gr.Image(label="Kết quả phân tích", elem_id=f"{input_source_name}_output")
        result_text = gr.Textbox(label="Chi tiết kết quả", lines=4, elem_id=f"{input_source_name}_result")
        
        # Save button
        save_button = gr.Button("Lưu kết quả phân tích này")
        save_status = gr.Textbox(label="Trạng thái lưu", elem_id=f"{input_source_name}_save_status")
        
        # Thiết lập sự kiện phân tích ảnh
        analyze_button.click(
            process_image,
            inputs=image_input,
            outputs=[image_output, result_text]
        )
        
        return image_input, image_output, result_text, save_button, save_status