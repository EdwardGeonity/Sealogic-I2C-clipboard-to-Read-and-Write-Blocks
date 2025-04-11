# Sealogic-I2C-clipboard-to-Read-and-Write-Blocks

![Sealogic I2C clipboard to Read and Write Blocks](https://github.com/user-attachments/assets/ea6d842b-1ab6-4762-8a8c-8c77d775485e)


 Sealogic I2C Clipboard Parser

This Python script processes clipboard-copied I2C logs from Sealogic logic analyzer software. It extracts meaningful I2C communication blocks and organizes them into structured write (WBlock) and read (RBlock) command sequences.
🧩 Features:

    Parses raw Sealogic clipboard logs (I2C start, address, data, stop lines).

    Groups I2C data into blocks based on start-stop sequences and read/write flags.

    Detects device address and formats write blocks like:

WBlock(2D) = [
    (0x0103, 0x01, 1),
    ...
]

Read commands are saved as:

    RBlock(2D) = [
        (0x0100, 1),
        ...
    ]

    Automatically detects and logs gaps between register addresses (optional).

    Saves output as a .txt file named after the device address.

🛠 Use Case:

Perfect for reverse engineering I2C sensor configs, firmware debug, or capturing device initialization sequences from raw Sealogic clipboard output.
💡 How to Use:

    Copy raw I2C log from Sealogic analyzer clipboard.

    Run the script — it will:

        Parse the clipboard text.

        Extract I2C blocks by address.

        Save structured output to readable files.

📎 Example Input:

I2C start
address: 0x5A write
data: 0x01
data: 0x00
data: 0xFF
I2C stop

📄 Output:

Addr=5A
WBlock(5A) = [
    (0x0100, 0xFF, 1)
]

