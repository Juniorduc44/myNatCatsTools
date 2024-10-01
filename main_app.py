import customtkinter as ctk
import time
import threading
import block_fetcher
import block_fetcher2

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BlockSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bitcoin Block Search")
        self.geometry("600x550")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

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

        # Fetcher Switch
        self.fetcher_var = ctk.StringVar(value="API")
        self.fetcher_switch = ctk.CTkSwitch(self, text="Use Local Node", 
                                            variable=self.fetcher_var, 
                                            onvalue="RPC", offvalue="API")
        self.fetcher_switch.grid(row=1, column=0, padx=10, pady=10)

        # Search Button
        self.search_button = ctk.CTkButton(self, text="Search", command=self.start_search)
        self.search_button.grid(row=2, column=0, padx=10, pady=10)

        # Counter Label
        self.counter_label = ctk.CTkLabel(self, text="0/0 blocks with natcats")
        self.counter_label.grid(row=3, column=0, padx=10, pady=5)

        # Results Text Box
        self.results_text = ctk.CTkTextbox(self, width=580, height=300)
        self.results_text.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

    def start_search(self):
        start = int(self.start_block.get())
        end = int(self.end_block.get())
        self.search_button.configure(state="disabled")
        self.results_text.delete("0.0", ctk.END)
        threading.Thread(target=self.search_blocks, args=(start, end), daemon=True).start()

    def search_blocks(self, start_block, end_block):
        natcat_count = 0
        total_count = 0

        use_rpc = self.fetcher_var.get() == "RPC"
        fetcher = block_fetcher2.fetch_block_data if use_rpc else block_fetcher.fetch_block_data
        delay = 2 if use_rpc else 11  # 2 seconds for RPC, 11 seconds for API

        for height in range(start_block, end_block + 1):
            self.update_results(f"Checking block {height}...\n")
            block_data = fetcher(height)
            if block_data:
                bits = block_data.get('bits') if use_rpc else block_data['blocks'][0]['bits']
                if self.check_bits_for_3b(bits):
                    natcat_count += 1
                    self.update_results(f"Block {height}: bits = {bits}\n")
                else:
                    self.update_results(f"Block {height}: No natcat found\n")
            else:
                self.update_results(f"Block {height}: Data not found\n")
            total_count += 1
            self.update_counter(natcat_count, total_count)
            time.sleep(delay)  # Wait between queries

        self.search_button.configure(state="normal")

    def check_bits_for_3b(self, bits):
        if isinstance(bits, int):
            hex_bits = hex(bits)[2:]
        else:
            hex_bits = bits
        return "3b" in hex_bits.lower()

    def update_results(self, text):
        self.results_text.configure(state="normal")
        self.results_text.insert(ctk.END, text)
        self.results_text.configure(state="disabled")
        self.results_text.see(ctk.END)

    def update_counter(self, natcat_count, total_count):
        self.counter_label.configure(text=f"{natcat_count}/{total_count} blocks with natcats")

if __name__ == "__main__":
    app = BlockSearchApp()
    app.mainloop()