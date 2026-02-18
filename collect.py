import asyncio
from datetime import datetime
from bleak import BleakClient

# =============================================
# CHANGE THESE TWO LINES ONLY
ADDRESS   = "cd:d1:fd:5c:dd:58"   # your BLE address
CSV_PATH  = "stairs_down.csv"            # change to "flex.csv" for second gesture
# =============================================

CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

def int16_le(b0, b1):
    return int.from_bytes(bytes([b0, b1]), byteorder="little", signed=True)

def handle_notify(sender, data: bytearray):
    if len(data) != 8:
        return
    ax_g = int16_le(data[2], data[3]) / 1000.0
    ay_g = int16_le(data[4], data[5]) / 1000.0
    az_g = int16_le(data[6], data[7]) / 1000.0
    line = f"{ax_g:.3f},{ay_g:.3f},{az_g:.3f}"
    print(line)
    with open(CSV_PATH, "a") as f:
        f.write(line + "\n")

async def main():
    # Write header if file is new
    try:
        open(CSV_PATH, "r").close()
    except FileNotFoundError:
        with open(CSV_PATH, "w") as f:
            f.write("aX,aY,aZ\n")

    print(f"Connecting to {ADDRESS} ...")
    async with BleakClient(ADDRESS) as client:
        print("Connected! Perform gestures now. Ctrl+C to stop.")
        await client.start_notify(CHAR_UUID, handle_notify)
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped. Data saved to", CSV_PATH)
