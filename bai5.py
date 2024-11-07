n = int(input("Nhập số nguyên n (n > 0): "))
tong = sum(i / (i + 1) for i in range(1, n + 1))
print("Tổng của dãy là:", tong)