def print_hex_range(start, end):
    for bit in range(start, end + 1):
        print(f"Bit {bit}: {hex(bit)}")

while True:
    print(END2, "***it works***")
    try:
        start = int(input("Enter starting bit number (1-830592): "))
        end = int(input("Enter ending bit number (1-830592): "))
        
        if 1 <= start <= end <= 830592:
            print_hex_range(start, end)
            break
        else:
            print("Invalid range. Please ensure start <= end and both are between 1 and 830592.")
    except ValueError:
        print("Invalid input. Please enter integers only.")
