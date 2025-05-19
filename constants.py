# Cấu hình và Hằng số
EMOTION_MAP_VIETNAMESE = {
    'happy': 'Vui vẻ',
    'sad': 'Buồn',
    'angry': 'Tức giận',
    'neutral': 'Trung lập',
    'surprise': 'Ngạc nhiên',
    'disgust': 'Ghê tởm',
    'fear': 'Sợ hãi'
}

SATISFACTION_LEVELS = {
    "Hài lòng": "😊",
    "Bình thường": "😐",
    "Không hài lòng": "😞"
}
FONTS = {
    "default": {
        "font_path": "fonts/arial.ttf",
        "font_size": 20,
        "color": (255, 255, 255)
    },
}
# Đường dẫn file log
import os
LOG_FILE_PATH = os.path.join("data", "emotion_log.csv")

# Đảm bảo thư mục data tồn tại
os.makedirs("data", exist_ok=True)