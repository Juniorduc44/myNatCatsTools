import requests
import time

def fetch_block_data(block_height):
    url = f"https://blockchain.info/block-height/{block_height}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_bits_for_3b(bits):
    # Convert integer to hexadecimal string
    hex_bits = hex(bits)[2:]  # [2:] to remove '0x' prefix
    return "3b" in hex_bits.lower()

def find_3b_blocks(start_block, end_block):
    found_blocks = []
    for height in range(start_block, end_block + 1):
        print(f"Checking block {height}...")
        block_data = fetch_block_data(height)
        if block_data:
            bits = block_data['blocks'][0]['bits']
            if check_bits_for_3b(bits):
                found_blocks.append((height, hex(bits)[2:]))
                print(f"Found matching block: {height}, bits: {hex(bits)[2:]}")
        time.sleep(11)  # Wait for 3 seconds between queries
    return found_blocks

def main():
    start_block = int(input("Enter the starting block height: "))
    end_block = int(input("Enter the ending block height: "))
    
    print(f"Searching for blocks with '3b' in the bits field from block {start_block} to {end_block}...")
    matching_blocks = find_3b_blocks(start_block, end_block)
    
    print("\nResults:")
    if matching_blocks:
        for height, bits in matching_blocks:
            print(f"Block {height}: bits = {bits}")
    else:
        print("No blocks found with '3b' in the bits field in the specified range.")

if __name__ == "__main__":
    main()