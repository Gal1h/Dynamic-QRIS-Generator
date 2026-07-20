import qrcode
import sys
import os

#QRCode
STATIC_QRIS = "00020101021126610016ID.CO.SHOPEE.WWW01189360091800229523010208229523010303UMI51440014ID.CO.QRIS.WWW0215ID10265078185930303UMI5204581753033605802ID5911Vyson Store6010TRENGGALEK61056636162070703A01630477AE"
#default output folder
Save_Folder = "output"

#Create folder if not exist
if not os.path.exists(Save_Folder):
    os.makedirs(Save_Folder)

def calculate_crc16(payload: str) -> str:
    #Calculates the CRC-16 (CCITT-FALSE) checksum required by the EMVCo standard.
    crc = 0xFFFF
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
            crc &= 0xFFFF
    
    # Return as a 4-character uppercase hexadecimal string
    return f"{crc:04X}"

def generate_dynamic_qris(base_qris: str, amount: int) -> str:
    #Injects an amount into a static QRIS string and recalculates the CRC.
    
    # 1. Strip the existing CRC tag (63) and its value (last 8 characters)
    if not base_qris[-8:-4] == "6304":
        raise ValueError("Invalid QRIS format: Missing '6304' CRC tag at the end.")
    
    payload_without_crc = base_qris[:-8]
    
    # 2. Change Point of Initiation (Tag 01) from 11 (Static) to 12 (Dynamic)
    # The string starts with 000201 (Format Indicator), followed by 010211
    if payload_without_crc.startswith("000201010211"):
        payload_without_crc = payload_without_crc.replace("010211", "010212", 1)
        
    # 3. Format the amount for Tag 54
    # Format: 54 + [2-digit length] + [amount]
    str_amount = str(amount)
    amount_tag = f"54{len(str_amount):02d}{str_amount}"
    
    # 4. Append the amount tag and the CRC header (6304)
    new_payload = payload_without_crc + amount_tag + "6304"
    
    # 5. Calculate the new CRC checksum
    new_crc = calculate_crc16(new_payload)
    
    # 6. Return the complete dynamic QRIS string
    return new_payload + new_crc

def create_qr_image(qris_string: str, filename: str):
    #Generates a QR code image from the QRIS string
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qris_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{Save_Folder}/{filename}")
    print(f"Success! QR code saved as {filename}")

if __name__ == "__main__":
    try:
        amount = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        
        print(f"Generating Dynamic QRIS for Rp {amount}...")
        
        # Generate the new string
        dynamic_qris = generate_dynamic_qris(STATIC_QRIS, amount)
        print(f"\nNew QRIS String:\n{dynamic_qris}\n")
        
        # Create the image file
        filename = f"qris_{amount}.png"
        create_qr_image(dynamic_qris, filename)
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Usage: python qris_generator.py [amount]")
