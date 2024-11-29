def dao_nguoc_cac_tu(chuoi):
    tu_dao_nguoc = chuoi.split()[::-1] 
    return " ".join(tu_dao_nguoc)      

chuoi = input("Nhập chuỗi: ")
print("Chuỗi đảo ngược là:", dao_nguoc_cac_tu(chuoi))
