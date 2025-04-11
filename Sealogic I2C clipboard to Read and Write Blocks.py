import os
import tkinter as tk
from tkinter import filedialog

def parse_i2c_log(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]

    cmds = []
    pending_reg = {}
    state = None   # None, 'W', 'R'
    addr = None
    buf = []

    for parts in (line.split() for line in lines):
        if parts[0] != 'I2C':
            continue

        kw = parts[1].lower()
        if kw == 'start':
            state = None
            buf = []

        elif kw == 'address':
            a = parts[2].replace('0x','').upper()
            is_read = parts[3].lower() == 'true'
            addr = a
            state = 'R' if is_read else 'W'
            buf = []

        elif kw == 'data' and state in ('W','R'):
            val = parts[-1].replace('0x','').upper().zfill(2)
            buf.append(val)

        elif kw == 'stop' and state:
            if state == 'W' and len(buf) >= 2:
                reg = buf[0] + buf[1]
                data = buf[2:]
                cmds.append((addr, 'W', reg, data, len(data)))
                pending_reg[addr] = reg
            elif state == 'R' and buf:
                reg = pending_reg.get(addr, '0000')
                cmds.append((addr, 'R', reg, buf, len(buf)))
            state = None
            buf = []

    return cmds

def group_sequence(cmds):
    blocks = []
    current = None
    for addr, op, reg, data_list, length in cmds:
        if current is None or addr!=current[0] or op!=current[1]:
            if current:
                blocks.append(tuple(current))
            current = [addr, op, []]
        current[2].append((reg, data_list, length))
    if current:
        blocks.append(tuple(current))
    return blocks

def write_blocks(blocks, name, input_path):
    folder = os.path.dirname(input_path)
    base = os.path.splitext(os.path.basename(input_path))[0]
    out = os.path.join(folder, f"{base}_Wb.txt")

    counters = {}
    with open(out, 'w', encoding='utf-8') as f:
        for addr, op, buf in blocks:
            counters.setdefault((addr,op),0)
            counters[(addr,op)] +=1
            idx = counters[(addr,op)]
            f.write(f"Addr={addr}\n")
            blk = 'WBlock' if op=='W' else 'RBlock'
            f.write(f"{blk}({idx}, {name}) = [\n")
            for reg, data_list, length in buf:
                ds = ''.join(data_list)
                f.write(f"    ({reg}, {ds}, {length})\n")
            f.write("]\n\n")
    print(f"Saved: {out}")

def main():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Выберите I2C лог-файлы (*.txt)",
        filetypes=[("Text Files", "*.txt")])
    if not file_paths:
        print("Файлы не выбраны, выходим.")
        return

    for path in file_paths:
        print(f"\nProcessing: {path}")
        cmds = parse_i2c_log(path)
        blocks = group_sequence(cmds)
        name = os.path.splitext(os.path.basename(path))[0]
        write_blocks(blocks, name, path)

    print("\nВсе файлы обработаны.")

if __name__ == "__main__":
    main()
