import os
from pydub import AudioSegment

# 設定
input_folder = r"C:\Users\nagna\MyProject\input_clips"    # 分割済みクリップが保存されているフォルダのパスを指定してください
output_folder = r"C:\Users\nagna\MyProject\output_clips"  # マージ後のファイルを保存するフォルダのパスを指定してください
min_duration_ms = 3000  # 最低3秒（3000ミリ秒）

# 出力フォルダが存在しなければ作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 入力フォルダ内の.wavファイルを取得し、順番にソート（ファイル名に番号がある場合は順番通りに処理されます）
files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(".wav")])

merged_audio = AudioSegment.empty()
file_counter = 1

for filename in files:
    file_path = os.path.join(input_folder, filename)
    clip = AudioSegment.from_file(file_path)
    
    # 現在のクリップを連結
    merged_audio += clip

    # 連結後の長さが最低3秒以上なら出力
    if len(merged_audio) >= min_duration_ms:
        output_filename = f"merged_{file_counter:03d}.wav"
        output_path = os.path.join(output_folder, output_filename)
        merged_audio.export(output_path, format="wav")
        print(f"Exported: {output_filename} ({len(merged_audio)/1000:.2f}秒)")
        merged_audio = AudioSegment.empty()
        file_counter += 1

# ループ終了後、余りが残っている場合は別ファイルとして出力
if len(merged_audio) > 0:
    output_filename = f"merged_{file_counter:03d}.wav"
    output_path = os.path.join(output_folder, output_filename)
    merged_audio.export(output_path, format="wav")
    print(f"Exported (remainder): {output_filename} ({len(merged_audio)/1000:.2f}秒)")
