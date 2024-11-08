import re
import pandas as pd
from docx import Document # type: ignore
from docx.shared import RGBColor # type: ignore

# Đường dẫn đến file Word và file Excel xuất ra
input_docx = r'D:\jvb\JVB-python\convert\4.docx'
output_excel = r'D:\jvb\JVB-python\convert\output.xlsx'

# Tải tài liệu Word
doc = Document(input_docx)

# Khởi tạo danh sách để lưu trữ dữ liệu
questions = []
all_answers = []
correct_answers = []

# Hàm kiểm tra nếu `run` có màu đỏ
def is_red(run):
    return run.font.color and run.font.color.rgb == RGBColor(255, 0, 0)

current_answers = []  # Lưu đáp án cho câu hiện tại
current_correct_answer = None  # Đáp án đúng
is_first_paragraph = True  # Bỏ qua tiêu đề


for para in doc.paragraphs:
    # Bỏ qua tiêu đề
    if is_first_paragraph:
        is_first_paragraph = False
        continue

    # Kiểm tra câu hỏi nếu có chữ in đậm
    if any(run.bold for run in para.runs):
        # Lưu câu hỏi và đáp án của câu trước nếu có
        if current_answers:
            all_answers.append(current_answers)
            correct_answers.append(current_correct_answer)
            current_answers = []
            current_correct_answer = None
        questions.append(para.text.strip())
    elif re.match(r'^[A-D]\.', para.text.strip()):
        # Thêm đáp án vào danh sách
        answer_text = para.text.strip()
        current_answers.append(answer_text)

        # Kiểm tra nếu có ít nhất một `run` màu đỏ trong đáp án
        red_runs = [run.text for run in para.runs if is_red(run)]
        if red_runs and current_correct_answer is None:
            # Nếu có `run` màu đỏ, ghép các phần có màu đỏ lại thành đáp án đúng
            current_correct_answer = ''.join(red_runs).strip()
    elif para.text.strip() == "":
        # Nếu gặp đoạn trống, lưu các đáp án của câu hiện tại
        if current_answers:
            all_answers.append(current_answers)
            correct_answers.append(current_correct_answer)
            current_answers = []
            current_correct_answer = None

# Kiểm tra nếu còn câu hỏi hoặc đáp án chưa lưu
if current_answers:
    all_answers.append(current_answers)
    correct_answers.append(current_correct_answer)

# Chuẩn bị dữ liệu cho DataFrame
data_length = max(len(questions), len(all_answers), len(correct_answers))
data = {
    "STT": range(1, data_length + 1),
    "Chủ đề": ["BÀI LUYỆN TẬP TRẮC NGHIỆM SỐ 4"] * data_length,
    "Câu hỏi": questions + [""] * (data_length - len(questions)),
    "Câu trả lời": all_answers + [[]] * (data_length - len(all_answers)),
    "Câu trả lời đúng": correct_answers + [""] * (data_length - len(correct_answers)),
    "Dạng đáp án": ["Không hình ảnh"] * data_length,
    "Random câu trả lời": ["Không đảo câu trả lời"] * data_length,
    "Link ảnh đáp án": [""] * data_length
}

# Chuyển đổi danh sách đáp án thành chuỗi, ngăn cách bằng dấu xuống dòng
df = pd.DataFrame(data)
df["Câu trả lời"] = df["Câu trả lời"].apply(lambda x: "\n".join(x) if isinstance(x, list) else x)

# Xuất ra file Excel
with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    worksheet = writer.sheets['Sheet1']

    lend = 20 # moocs
    # Thiết lập độ rộng cho cột trong Excel
    worksheet.set_column('A:A', lend - 10)   # STT
    worksheet.set_column('B:B', lend - 10)  # Chủ đề
    worksheet.set_column('C:C', 50)  # Câu hỏi
    worksheet.set_column('D:D', 50)  # Câu trả lời
    worksheet.set_column('E:E', lend - 30)  # Câu trả lời đúng
    worksheet.set_column('F:F', 15)  # Dạng đáp án
    worksheet.set_column('G:G', lend)  # Random câu trả lời
    worksheet.set_column('H:H', lend)  # Link ảnh đáp án

print(f"Dữ liệu đã được xuất thành công vào {output_excel}")
