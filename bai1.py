
# n = int(input("Nhập số nguyên n: "))
# tong_chan = sum(i for i in range(2, n+1, 2))
# print("Tổng của tất cả các số chẵn từ 1 đến", n, "là:", tong_chan)

n = int(input("Nhập số nguyên n: "))
tong_chan = 0
for i in range(n+1):
    if i % 2 == 0:
        tong_chan = i + tong_chan
print("Tổng của tất cả các số chẵn từ 1 đến", n, "là:", tong_chan)

