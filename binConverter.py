import sys
import binascii
import os
from tqdm import tqdm  # Import tqdm for progress bar

def read_file_in_chunks(filename, chunk_size=128):
    """Reads a file in chunks and yields each byte with a progress bar."""
    file_size = os.stat(filename).st_size
    with open(filename, "rb") as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Reading file") as pbar:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    yield from chunk
                    pbar.update(len(chunk))
                else:
                    break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('usage: binConverter.py "pathToFile\\fileName.bin"')

    file_in = sys.argv[1]
    base, _ = os.path.splitext(file_in)
    file_out = "hekate_ctcaer.h"

    string_buffer = "\t"
    byte_count = 0
    print("reading file: " + file_in)

    for byte in read_file_in_chunks(file_in, 16):
        byte_count += 1
        string_buffer += "0x" + binascii.hexlify(bytes([byte])).decode('ascii') + ", "
        if byte_count % 16 == 0:
            string_buffer += "\n\t"

    string_buffer = (
        "#include <Arduino.h> \n \n \n"
        "// Generated using " + base + ".bin\n"
        f"#define FUSEE_BIN_SIZE {byte_count}\n"
        f"const PROGMEM byte fuseeBin[FUSEE_BIN_SIZE] = {{\n{string_buffer}\n}};"
    )

    print("\nwriting file: " + file_out)
    with open(file_out, "w") as text_file:
        text_file.write(string_buffer)

    print("finished")