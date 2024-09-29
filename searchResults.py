import customtkinter
import re

class HexSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Hex Search Tool")
        master.geometry("600x400")

        self.frame = customtkinter.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.search_var = customtkinter.StringVar()
        self.search_var.trace("w", self.on_search_change)

        self.search_entry = customtkinter.CTkEntry(
            self.frame, 
            placeholder_text="Enter number to search...",
            textvariable=self.search_var,
            width=200
        )
        self.search_entry.pack(pady=10, padx=10)

        self.result_text = customtkinter.CTkTextbox(self.frame, height=300)
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)

        self.load_data()

    def load_data(self):
        with open("result.txt", "r") as file:
            self.data = file.readlines()

    def on_search_change(self, *args):
        search_term = self.search_var.get()
        if search_term:
            results = self.search_data(search_term)
            self.display_results(results)
        else:
            self.result_text.delete("1.0", customtkinter.END)

    def search_data(self, term):
        pattern = re.compile(r'\b' + re.escape(term))
        return [line.strip() for line in self.data if pattern.search(line)]

    def display_results(self, results):
        self.result_text.delete("1.0", customtkinter.END)
        for result in results:
            self.result_text.insert(customtkinter.END, result + "\n")

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = HexSearchApp(root)
    root.mainloop()