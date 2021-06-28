if __name__ == "__main__":
    sum_ = 0
    for i in range(101):
        sum_ += i
    print(f"For 迴圈 1~100 : = {sum_}")
    
    sum_ = 0
    i = 1
    while i <= 100:
        sum_ += i
        i += 1
    print(f"While 迴圈 1~100 : = {sum_}")
    
    # Advanced solution - List comprehension
    print(f"List comprehension 1~100: {sum([i for i in range(101)])}")