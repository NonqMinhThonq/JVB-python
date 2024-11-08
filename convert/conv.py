import os
import re
import pandas as pd
from docx import Document  # type: ignore
from docx.shared import RGBColor  # type: ignore

# Lấy đường dẫn của thư mục chứa file mã hiện tại
base_folder = os.path.dirname(__file__)

# CR3: Tự động phát hiện file .docx trong thư mục
docx_files = [f for f in os.listdir(base_folder) if f.endswith('.docx')]
if len(docx_files) != 1:
    raise FileNotFoundError("Không tìm thấy file .docx trong thư mục...")
input_docx = os.path.join(base_folder, docx_files[0])

# CR2: Lấy tên file (không có phần mở rộng) làm tên chủ đề
file_name = os.path.splitext(docx_files[0])[0]

# Đường dẫn output Excel
output_excel = os.path.join(base_folder, "output.xlsx")

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

# Phân tích tài liệu
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

        # Loại bỏ số thứ tự (1., 2., 3., ...) ở đầu câu hỏi
        question_text = re.sub(r'^\d+\.\s*', '', para.text.strip())
        questions.append(question_text)
    
    elif re.match(r'^[A-D]\.', para.text.strip()):
        # Loại bỏ ký hiệu đầu dòng (A., B., C., D.) khỏi đáp án
        answer_text = re.sub(r'^[A-D]\.\s*', '', para.text.strip())
        current_answers.append(answer_text)

        # Kiểm tra nếu có ít nhất một `run` màu đỏ trong đáp án
        red_runs = [run.text for run in para.runs if is_red(run)]
        if red_runs and current_correct_answer is None:
            # Nếu có `run` màu đỏ, ghép các phần có màu đỏ lại thành đáp án đúng và loại bỏ ký hiệu đầu
            combined_red_text = ''.join(red_runs).strip()
            current_correct_answer = re.sub(r'^[A-D]\.\s*', '', combined_red_text)
    
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
    "Chủ đề": [file_name] * data_length,  # CR2: Sử dụng tên file làm tên chủ đề
    "Câu hỏi": questions + [""] * (data_length - len(questions)),
    "Câu trả lời": all_answers + [[]] * (data_length - len(all_answers)),
    "Câu trả lời đúng": correct_answers + [""] * (data_length - len(correct_answers)),
    "Dạng đáp án": ["Không hình ảnh"] * data_length,
    "Random câu trả lời": ["Không đảo câu trả lời"] * data_length,
    "Link ảnh đáp án": [""] * data_length
}

# Chuyển đổi danh sách đáp án thành chuỗi, ngăn cách bằng dấu xuống dòng
# Loại bỏ tất cả các ký hiệu "A.", "B.", "C.", "D." khỏi từng đáp án trong danh sách đáp án
def remove_choice_prefix_from_text(text):
    return re.sub(r'\b[A-D]\.\s*', '', text)

df = pd.DataFrame(data)
df["Câu trả lời"] = df["Câu trả lời"].apply(lambda answers: "\n".join(
    [remove_choice_prefix_from_text(answer) for answer in answers]
) if isinstance(answers, list) else answers)

# Xuất ra file Excel
with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    worksheet = writer.sheets['Sheet1']

    lend = 20
    # Thiết lập độ rộng cho cột trong Excel
    worksheet.set_column('A:A', lend - 10)   # STT
    worksheet.set_column('B:B', lend - 10)  # Chủ đề
    worksheet.set_column('C:C', 50)  # Câu hỏi
    worksheet.set_column('D:D', 50)  # Câu trả lời
    worksheet.set_column('E:E', lend + 30)  # Câu trả lời đúng
    worksheet.set_column('F:F', 15)  # Dạng đáp án
    worksheet.set_column('G:G', lend)  # Random câu trả lời
    worksheet.set_column('H:H', lend)  # Link ảnh đáp án

print(f"Dữ liệu đã được xuất thành công vào {output_excel}")
