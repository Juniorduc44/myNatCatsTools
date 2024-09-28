import customtkinter

def print_hex_range(start, end):
    result = ""
    for bit in range(start, end + 1):
        result += f"Bit {bit}: {hex(bit)}\n"
    return result

def button_function():
    try:
        start = int(start_entry.get().replace(',', ''))
        end = int(end_entry.get().replace(',', ''))
        
        if 1 <= start <= end <= 830592:
            result = print_hex_range(start, end)
            result_text.delete("1.0", customtkinter.END)
            result_text.insert("1.0", result)
        else:
            result_text.delete("1.0", customtkinter.END)
            result_text.insert("1.0", "Invalid range. Please ensure start <= end and both are between 1 and 830592.")
    except ValueError:
        result_text.delete("1.0", customtkinter.END)
        result_text.insert("1.0", "Invalid input. Please enter integers only.")

app = customtkinter.CTk()
app.geometry("500x400")
app.title("NatCats Hex Range Tool")

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=10, padx=15, expand=True, fill="both")

label = customtkinter.CTkLabel(master=frame, justify=customtkinter.LEFT, text="NatsCats Hex Range Finder")
label.pack(pady=10, padx=10)

start_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter starting bit # (1-830592)")
start_entry.pack(padx=25, pady=10)

end_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter ending bit # (1-830592)")
end_entry.pack(padx=25, pady=10)

convert_button = customtkinter.CTkButton(master=frame, text="Convert", command=button_function)
convert_button.pack(padx=25, pady=10)

result_text = customtkinter.CTkTextbox(master=frame, height=150)
result_text.pack(padx=25, pady=10, expand=True, fill="both")

app.mainloop()