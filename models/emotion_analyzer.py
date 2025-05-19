import cv2
import numpy as np
from deepface import DeepFace
from datetime import datetime
from constants import EMOTION_MAP_VIETNAMESE, SATISFACTION_LEVELS, FONTS
import freetype

def put_vietnamese_text(img, text, position, font_path, font_size, color):
    """Vẽ text tiếng Việt lên ảnh sử dụng freetype"""
    font = freetype.Face(font_path)
    font.set_char_size(font_size * 64)
    
    x, y = position
    for char in text:
        font.load_char(char)
        bitmap = font.glyph.bitmap
        h, w = bitmap.rows, bitmap.width
        
        glyph_pixels = np.array(bitmap.buffer, dtype=np.uint8).reshape(h, w)
        
        # Tìm vị trí để vẽ ký tự
        top = y - font.glyph.bitmap_top
        left = x + font.glyph.bitmap_left
        
        # Đặt ký tự lên ảnh với màu tương ứng
        for i in range(h):
            for j in range(w):
                if 0 <= top + i < img.shape[0] and 0 <= left + j < img.shape[1]:
                    if glyph_pixels[i, j]:
                        img[top + i, left + j] = color
        
        # Di chuyển đến vị trí ký tự tiếp theo
        x += (font.glyph.advance.x >> 6)

def map_emotion_to_satisfaction(emotion_eng):
    """Ánh xạ cảm xúc tiếng Anh sang mức độ hài lòng và icon."""
    if emotion_eng in ['happy', 'surprise']:
        return "Hài lòng", SATISFACTION_LEVELS["Hài lòng"]
    elif emotion_eng in ['neutral']:
        return "Bình thường", SATISFACTION_LEVELS["Bình thường"]
    elif emotion_eng in ['sad', 'angry', 'disgust', 'fear']:
        return "Không hài lòng", SATISFACTION_LEVELS["Không hài lòng"]
    else:
        return "Không xác định", "❓"

def analyze_face_emotions(image):
    """
    Phân tích khuôn mặt và cảm xúc từ ảnh.
    Trả về: ảnh đã vẽ bounding box và nhãn, danh sách các kết quả phân tích.
    """
    results = []
    
    # Chuyển đổi ảnh về định dạng NumPy nếu cần
    if isinstance(image, str):  # Nếu là đường dẫn ảnh
        img_to_draw = cv2.imread(image)
        image_np = cv2.cvtColor(img_to_draw, cv2.COLOR_BGR2RGB)
    elif isinstance(image, np.ndarray):  # Nếu là mảng NumPy
        image_np = image.copy()
        if image_np.shape[2] == 3 and image_np.dtype == np.uint8:
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                # Chuyển BGR sang RGB nếu cần
                if cv2.cvtColor(image_np[:1, :1, :], cv2.COLOR_BGR2RGB).any() != image_np[:1, :1, :].any():
                    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        img_to_draw = image_np.copy()
    else:
        return None, []  # Trả về None nếu không hỗ trợ định dạng ảnh

    try:
        # DeepFace.analyze có thể phát hiện nhiều khuôn mặt
        analysis = DeepFace.analyze(
            img_path=image_np,
            actions=['emotion'],
            enforce_detection=True,
            detector_backend='opencv'
        )

        # DeepFace.analyze trả về list nếu có nhiều khuôn mặt, dict nếu có 1
        if isinstance(analysis, list):
            face_detections = analysis
        else:
            face_detections = [analysis]

        for face_info in face_detections:
            region = face_info['region']  # x, y, w, h
            dominant_emotion_eng = face_info['dominant_emotion']
            emotion_vn = EMOTION_MAP_VIETNAMESE.get(dominant_emotion_eng, dominant_emotion_eng)
            satisfaction_vn, satisfaction_icon = map_emotion_to_satisfaction(dominant_emotion_eng)
            font_path = FONTS["default"]["font_path"]
            # Vẽ bounding box
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            cv2.rectangle(img_to_draw, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Chuẩn bị text để hiển thị
            label_text = f"{emotion_vn} ({satisfaction_vn} {satisfaction_icon})"

            # Đặt text phía trên bounding box
            text_y = y - 10 if y - 10 > 10 else y + h + 20
            # cv2.putText(img_to_draw, label_text, (x, text_y),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            put_vietnamese_text(img_to_draw, label_text, (x, text_y), font_path, 20, (0, 255, 0))
            results.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dominant_emotion_eng": dominant_emotion_eng,
                "emotion_vn": emotion_vn,
                "satisfaction_vn": satisfaction_vn,
                "satisfaction_icon": satisfaction_icon,
                "facial_area": region
            })

    except ValueError as e:
        if "Face could not be detected" in str(e) or "No face detected" in str(e):
            cv2.putText(img_to_draw, "Không phát hiện khuôn mặt", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Không phát hiện khuôn mặt")
        else:
            cv2.putText(img_to_draw, f"Lỗi: {str(e)}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print(f"Lỗi phân tích: {e}")
    except Exception as e:
        cv2.putText(img_to_draw, "Lỗi không xác định", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        print(f"Lỗi không xác định: {e}")

    return img_to_draw, results