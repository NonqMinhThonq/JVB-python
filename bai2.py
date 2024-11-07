def kiem_tra_nguyen_to(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

n = int(input("Nhập một số nguyên: "))
if kiem_tra_nguyen_to(n):
    print(n, "là số nguyên tố.")
else:
    print(n, "không phải là số nguyên tố.")
