import numpy as np
from models.emotion_analyzer import analyze_face_emotions

# Biến toàn cục lưu kết quả phân tích gần nhất
current_results = []

def process_image(image):
    """
    Xử lý ảnh từ webcam hoặc ảnh được tải lên.
    """
    global current_results
    
    if image is None:
        return None, "Không có ảnh"
    
    # Chuyển đổi định dạng ảnh
    image_np = np.array(image)
    
    # Phân tích ảnh
    processed_image, results = analyze_face_emotions(image_np)
    
    # Lưu kết quả
    current_results = results
    
    # Tạo văn bản kết quả
    if results:
        analysis_text = "Kết quả phân tích:\n"
        for i, result in enumerate(results):
            analysis_text += f"- Người {i+1}: {result['emotion_vn']} - {result['satisfaction_vn']} {result['satisfaction_icon']}\n"
    else:
        analysis_text = "Không phát hiện khuôn mặt hoặc cảm xúc"
    
    return processed_image, analysis_text

def get_current_results():
    """Trả về kết quả phân tích hiện tại."""
    global current_results
    return current_results

def clear_current_results():
    """Xóa kết quả phân tích hiện tại."""
    global current_results
    current_results = []