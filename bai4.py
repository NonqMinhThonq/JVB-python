def dao_nguoc_cac_tu(chuoi):
    tu_dao_nguoc = chuoi.split()[::-1]  # Tách chuỗi thành các từ và đảo ngược thứ tự từ
    return " ".join(tu_dao_nguoc)       # Ghép lại các từ đã đảo ngược thành chuỗi

chuoi = input("Nhập chuỗi: ")
print("Chuỗi đảo ngược là:", dao_nguoc_cac_tu(chuoi))
