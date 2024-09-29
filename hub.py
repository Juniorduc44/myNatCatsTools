import customtkinter
import re

class HexSearchRangeHub:
    def __init__(self, master):
        self.master = master
        master.title("Hex Search and Range Finder Hub")
        master.geometry("800x600")

        self.frame = customtkinter.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Range Finder Section
        self.range_label = customtkinter.CTkLabel(self.frame, text="Hex Range Finder (3b Pattern)", font=("Arial", 16, "bold"))
        self.range_label.pack(pady=(10, 5))

        self.start_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter starting bit # (1-830592)")
        self.start_entry.pack(padx=25, pady=5)

        self.end_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter ending bit # (1-830592)")
        self.end_entry.pack(padx=25, pady=5)

        self.find_range_button = customtkinter.CTkButton(self.frame, text="Find 3b Pattern", command=self.find_range)
        self.find_range_button.pack(padx=25, pady=10)

        # Search Section
        self.search_label = customtkinter.CTkLabel(self.frame, text="Search Results", font=("Arial", 16, "bold"))
        self.search_label.pack(pady=(20, 5))

        self.search_var = customtkinter.StringVar()
        self.search_var.trace("w", self.on_search_change)

        self.search_entry = customtkinter.CTkEntry(
            self.frame, 
            placeholder_text="Enter number to search...",
            textvariable=self.search_var,
            width=200
        )
        self.search_entry.pack(pady=5, padx=10)

        # Results Display
        self.result_text = customtkinter.CTkTextbox(self.frame, height=300)
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

        self.data = []

    def find_range(self):
        try:
            start = int(self.start_entry.get().replace(',', ''))
            end = int(self.end_entry.get().replace(',', ''))
            
            if 1 <= start <= end <= 830592:
                result = self.print_hex_range(start, end)
                if result:
                    self.result_text.delete("1.0", customtkinter.END)
                    self.result_text.insert("1.0", result)
                    self.data = result.split('\n')
                else:
                    self.result_text.delete("1.0", customtkinter.END)
                    self.result_text.insert("1.0", "No results found with '3b' pattern in the given range.")
                    self.data = []
            else:
                self.result_text.delete("1.0", customtkinter.END)
                self.result_text.insert("1.0", "Invalid range. Please ensure start <= end and both are between 1 and 830592.")
                self.data = []
        except ValueError:
            self.result_text.delete("1.0", customtkinter.END)
            self.result_text.insert("1.0", "Invalid input. Please enter integers only.")
            self.data = []

    def print_hex_range(self, start, end):
        result = ""
        for bit in range(start, end + 1):
            hex_value = hex(bit)
            if "3b" in hex_value:
                result += f"Bit {bit}: {hex_value}\n"
        return result

    def on_search_change(self, *args):
        search_term = self.search_var.get()
        if search_term and self.data:
            results = self.search_data(search_term)
            self.display_results(results)
        else:
            self.result_text.delete("1.0", customtkinter.END)
            self.result_text.insert("1.0", "\n".join(self.data))

    def search_data(self, term):
        pattern = re.compile(r'\b' + re.escape(term))
        return [line.strip() for line in self.data if pattern.search(line)]

    def display_results(self, results):
        self.result_text.delete("1.0", customtkinter.END)
        for result in results:
            self.result_text.insert(customtkinter.END, result + "\n")

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = HexSearchRangeHub(root)
    root.mainloop()