import librosa
import os
import numpy as np

# Cấu hình trích xuất đặc trưng
SAMPLE_RATE = 16000  # Sample rate mong muốn (VIVOS thường là 16kHz)
N_MFCC = 40         # Số lượng hệ số MFCC
FRAME_LENGTH = 0.025 # Độ dài khung phân tích (25ms)
HOP_LENGTH = 0.010   # Bước nhảy giữa các khung (10ms)

def extract_mfcc(audio_path, sr=SAMPLE_RATE, n_mfcc=N_MFCC, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH):
    """
    Trích xuất MFCC từ một file audio.

    Args:
        audio_path (str): Đường dẫn đến file audio.
        sr (int): Sample rate mong muốn.
        n_mfcc (int): Số lượng hệ số MFCC.
        frame_length (float): Độ dài khung phân tích (giây).
        hop_length (float): Bước nhảy giữa các khung (giây).

    Returns:
        numpy.ndarray: Mảng numpy chứa các hệ số MFCC.  Shape là (n_mfcc, num_frames)
    """

    try:
        # 1. Đọc file audio bằng librosa
        y, sr = librosa.load(audio_path, sr=sr)

        # 2. Tính MFCC
        frame_length_samples = int(frame_length * sr)
        hop_length_samples = int(hop_length * sr)

        mfccs = librosa.feature.mfcc(y=y,
                                        sr=sr,
                                        n_mfcc=n_mfcc,
                                        n_fft=frame_length_samples, # n_fft là số điểm FFT, thường bằng frame_length
                                        hop_length=hop_length_samples,
                                        win_length=frame_length_samples) # win_length là độ dài cửa sổ, thường bằng frame_length

        return mfccs

    except Exception as e:
        print(f"Lỗi khi trích xuất MFCC từ {audio_path}: {e}")
        return None

def process_vivos_dataset(data_dir, transcript_file, output_dir):
    """
    Xử lý dataset VIVOS, trích xuất MFCC từ tất cả các file audio và lưu vào file .npy.

    Args:
        data_dir (str): Đường dẫn đến thư mục chứa dữ liệu audio (ví dụ: 'VIVOS/train').
        transcript_file (str): Đường dẫn đến file transcript (ví dụ: 'VIVOS/transcript/train.txt').
        output_dir (str): Đường dẫn đến thư mục để lưu các file MFCC (.npy).
    """

    # 1. Đọc transcript file để lấy danh sách file audio và văn bản tương ứng
    audio_paths = []
    transcripts = []

    with open(transcript_file, 'r', encoding='utf-8') as f:
        for line in f:
            filename, transcript = line.strip().split(" ", 1) # Tách filename và transcript
            audio_paths.append(os.path.join(data_dir, filename + ".wav"))
            transcripts.append(transcript)

    # 2. Tạo thư mục output nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 3. Duyệt qua danh sách file audio và trích xuất MFCC
    for i, audio_path in enumerate(audio_paths):
        try:
            mfccs = extract_mfcc(audio_path)

            if mfccs is not None:
                # Lưu MFCC vào file .npy
                output_filename = os.path.splitext(os.path.basename(audio_path))[0] + ".npy" # Lấy tên file audio không có đuôi
                output_path = os.path.join(output_dir, output_filename)
                np.save(output_path, mfccs)

                print(f"Đã trích xuất MFCC và lưu vào {output_path}")
            else:
                print(f"Không thể trích xuất MFCC từ {audio_path}")

        except Exception as e:
            print(f"Lỗi tổng quát khi xử lý {audio_path}: {e}")


