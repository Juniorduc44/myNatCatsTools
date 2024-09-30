import customtkinter as ctk
import requests
import time
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BlockSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NatCat Block Search")
        self.geometry("600x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(input_frame, text="Start Block:").grid(row=0, column=0, padx=5, pady=5)
        self.start_block = ctk.CTkEntry(input_frame)
        self.start_block.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(input_frame, text="End Block:").grid(row=0, column=2, padx=5, pady=5)
        self.end_block = ctk.CTkEntry(input_frame)
        self.end_block.grid(row=0, column=3, padx=5, pady=5)

        # Search Button
        self.search_button = ctk.CTkButton(self, text="Search", command=self.start_search)
        self.search_button.grid(row=1, column=0, padx=10, pady=10)

        # Counter Label
        self.counter_label = ctk.CTkLabel(self, text="0/0 blocks with natcats")
        self.counter_label.grid(row=2, column=0, padx=10, pady=5)

        # Results Text Box
        self.results_text = ctk.CTkTextbox(self, width=580, height=300)
        self.results_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    def start_search(self):
        start = int(self.start_block.get())
        end = int(self.end_block.get())
        self.search_button.configure(state="disabled")
        self.results_text.delete("1.0", ctk.END)
        threading.Thread(target=self.search_blocks, args=(start, end), daemon=True).start()

    def search_blocks(self, start_block, end_block):
        natcat_count = 0
        total_count = 0

        for height in range(start_block, end_block + 1):
            self.update_results(f"Checking block {height}...\n", "black")
            block_data = self.fetch_block_data(height)
            if block_data:
                bits = block_data['blocks'][0]['bits']
                if self.check_bits_for_3b(bits):
                    natcat_count += 1
                    self.update_results(f"Block {height}: bits = {hex(bits)[2:]}\n", "green")
                else:
                    self.update_results(f"Block {height}: No natcat found\n", "red")
            total_count += 1
            self.update_counter(natcat_count, total_count)
            time.sleep(11)  # Wait for 11 seconds between queries

        self.search_button.configure(state="normal")

    def fetch_block_data(self, block_height):
        url = f"https://blockchain.info/block-height/{block_height}?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def check_bits_for_3b(self, bits):
        hex_bits = hex(bits)[2:]
        return "3b" in hex_bits.lower()

    def update_results(self, text, color):
        self.results_text.insert(ctk.END, text)
        self.results_text.see(ctk.END)
        last_line_start = self.results_text.index(f"end-1c linestart")
        last_line_end = self.results_text.index(f"end-1c lineend")
        self.results_text.tag_add(color, last_line_start, last_line_end)
        self.results_text.tag_config(color, foreground=color)

    def update_counter(self, natcat_count, total_count):
        self.counter_label.configure(text=f"{natcat_count}/{total_count} blocks with natcats")

if __name__ == "__main__":
    app = BlockSearchApp()
    app.mainloop()