import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
def confirm(receiver, title, content):
    sender_email = "thongnmjvb@gmail.com"
    receiver_email = receiver
    password = "dier jzps wjor qjwm"  # Dùng App Password nếu xác minh 2 bước

    # Thiết lập email
    subject = title
    body = content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        # Khởi tạo kết nối SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        # Đo thời gian chỉ phần gửi email
        start_time = time.time()
        server.sendmail(sender_email, receiver_email, message.as_string())
        end_time = time.time()
        print("Email đã được gửi thành công!")
        print(f"gmail xacs thuc duoc gui trong khoang: {end_time - start_time:.2f} giây")
    except Exception as e:
        print("Có lỗi xảy ra:", e)
    finally:
        server.quit()  # Đảm bảo server luôn thoát

