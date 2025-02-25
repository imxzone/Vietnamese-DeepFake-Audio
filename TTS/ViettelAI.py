import requests
import json
import os

class ViettelAI:
    """
    Lớp để tương tác với API ViettelAI Text-to-Speech.
    """
    def __init__(self, token, output_dir="text_to_speech\output_audio\test_test"):
        """
        Khởi tạo lớp ViettelAI.

        Args:
            token (str): Token API của ViettelAI.
            output_dir (str, optional): Thư mục để lưu trữ file âm thanh. Mặc định là "text_to_speech\output_audio\test_test".
        """
        self.url = "https://viettelai.vn/tts/speech_synthesis"
        self.token = token
        self.output_dir = output_dir
        self.audio_format = "mp3"  # Cố định định dạng là mp3
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_audio(self, text, voice, output_file):
        """
        Tạo file âm thanh từ văn bản sử dụng API ViettelAI.

        Args:
            text (str): Văn bản cần chuyển đổi thành giọng nói.
            voice (str): Tên giọng đọc của ViettelAI.
            output_file (str): Đường dẫn đầy đủ đến file âm thanh đầu ra.
        """

        payload = json.dumps({
            "text": text,
            "voice": voice,
            "speed": 1,
            "tts_return_option": 2,
            "token": self.token,
            "without_filter": False,
        })
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", self.url, headers=headers, data=payload)
            response.raise_for_status()  # Báo lỗi nếu request không thành công

            with open(output_file, "wb") as file:
                file.write(response.content)

            print(f"Đã tạo file {output_file}")

        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi tạo âm thanh cho giọng {voice}: {e}")

    def process_text_and_generate_audio(self, text_file, voices):
        """
        Đọc file text và tạo file âm thanh cho mỗi dòng với từng giọng đọc.

        Args:
            text_file (str): Đường dẫn đến file text chứa các câu cần chuyển đổi.
            voices (list): Danh sách các giọng đọc của ViettelAI.
        """
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Không tìm thấy file {text_file}")
            return

        for voice in voices:
            voice_dir = os.path.join(self.output_dir, voice)
            os.makedirs(voice_dir, exist_ok=True)

            for i, line in enumerate(lines):
                text = line.strip()
                if text:
                    output_file = os.path.join(voice_dir, f"{voice}_{i + 1}.mp3") #Fix output về mp3
                    self.generate_audio(text, voice, output_file)