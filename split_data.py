import os
import argparse
import random
import shutil

def get_options():
    args = argparse.ArgumentParser()

    # Variables setting
    args.add_argument("--train-path", type=str, default="D:\\AI_Projects\\deepfakev3\\speech_to_text\\VIVOS\\train")  # Đường dẫn đến thư mục train
    args.add_argument("--dev-path", type=str, default="D:\\AI_Projects\\deepfakev3\\speech_to_text\\VIVOS\\dev")  # Đường dẫn đến thư mục dev
    args.add_argument("--dev-ratio", type=float, default=0.2, help="Tỷ lệ dữ liệu dev")

    opt = args.parse_args()

    return opt


def split_transcript(train_transcript_file, dev_ratio):
    """
    Chia file train.txt thành train_new.txt và dev.txt.

    Args:
        train_transcript_file (str): Đường dẫn đến file train.txt.
        dev_ratio (float): Tỷ lệ dữ liệu dev.
    """

    # 1. Đọc dữ liệu từ file train.txt
    data = []
    with open(train_transcript_file, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line.strip())

    # 2. Tính số lượng mẫu cho tập dev
    num_dev_samples = int(len(data) * dev_ratio)

    # 3. Chọn ngẫu nhiên các mẫu cho tập dev
    dev_samples = random.sample(data, num_dev_samples)

    # 4. Tạo tập train bằng cách loại bỏ các mẫu dev
    train_samples = [sample for sample in data if sample not in dev_samples]

    # 5. Ghi các mẫu train vào file train_new.txt
    new_train_transcript_file = train_transcript_file.replace("train.txt", "train_new.txt")
    with open(new_train_transcript_file, 'w', encoding='utf-8') as f:
        for sample in train_samples:
            f.write(sample + '\n')

    # 6. Ghi các mẫu dev vào file dev.txt
    dev_transcript_file = train_transcript_file.replace("train.txt", "dev.txt")
    with open(dev_transcript_file, 'w', encoding='utf-8') as f:
        for sample in dev_samples:
            f.write(sample + '\n')

    print(f"Đã chia transcript thành công!")
    print(f"File train mới: {new_train_transcript_file}")
    print(f"File dev: {dev_transcript_file}")

    return new_train_transcript_file, dev_transcript_file  # Trả về các đường dẫn file


def split_wav_files(opt, new_train_transcript_file, dev_transcript_file):
    """
    Di chuyển các file WAV từ thư mục train sang thư mục dev dựa trên thông tin trong file dev.txt.
    Giữ cấu trúc thư mục của speaker (VIVOSSPK01, VIVOSSPK02,...).

    Args:
        opt: Các options được cấu hình (chứa train_path, dev_path).
        new_train_transcript_file (str): Đường dẫn đến file train_new.txt.
        dev_transcript_file (str): Đường dẫn đến file dev.txt.
    """

    train_path = opt.train_path
    dev_path = opt.dev_path

    # 1. Tạo thư mục dev nếu chưa tồn tại
    if not os.path.exists(dev_path):
        os.makedirs(dev_path)

    # 2. Đọc các mẫu dev từ file dev.txt
    with open(dev_transcript_file, 'r', encoding='utf-8') as f:
        dev_samples = [line.strip() for line in f]  # Đọc vào một list

    # 3. Duyệt qua danh sách các speaker
    for i in range(1, 47):  # VIVOSSPK01 đến VIVOSSPK46
        speaker_id = f"VIVOSSPK{i:02}"  # Tạo ID của speaker (VIVOSSPK01, VIVOSSPK02,...)
        speaker_train_path = os.path.join(train_path, "waves", speaker_id)
        speaker_dev_path = os.path.join(dev_path, "waves", speaker_id)

        # Tạo thư mục speaker trong thư mục dev nếu chưa tồn tại
        if not os.path.exists(speaker_dev_path):
            os.makedirs(speaker_dev_path)

        # 4. Duyệt qua các file trong thư mục của speaker
        for filename in os.listdir(speaker_train_path):
            if filename.endswith(".wav"):
                filename_without_ext = filename[:-4]  # Loại bỏ phần mở rộng .wav

                # Kiểm tra xem file này có trong tập dev không
                is_dev_file = False
                for sample in dev_samples:
                    if sample.startswith(filename_without_ext): # Kiểm tra xem tên file có nằm trong dòng transcript dev
                        is_dev_file = True
                        break

                if is_dev_file:
                    # Di chuyển file sang thư mục dev
                    src_path = os.path.join(speaker_train_path, filename)
                    dest_path = os.path.join(speaker_dev_path, filename)

                    try:
                        shutil.move(src_path, dest_path) # Sử dụng shutil.move để di chuyển
                        print(f"Đã di chuyển: {src_path} -> {dest_path}")
                    except FileNotFoundError:
                        print(f"Không tìm thấy file: {src_path}")
                    except Exception as e:
                        print(f"Lỗi khi di chuyển {filename}: {e}")


    print("Đã di chuyển các file WAV thành công!")


def main():
    opt = get_options()

    # Đường dẫn đến file train.txt
    train_transcript_file = os.path.join(opt.train_path, "train.txt")

    # Chia file transcript
    new_train_transcript_file, dev_transcript_file = split_transcript(train_transcript_file, opt.dev_ratio)

    # Chia các file WAV
    split_wav_files(opt, new_train_transcript_file, dev_transcript_file)


if __name__ == "__main__":
    main()