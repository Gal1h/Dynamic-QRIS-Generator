# Dynamic QRIS Generator
easy python based dynamic QRIS generator


## Installation
```bash
git clone https://github.com/Gal1h/Dynamic-QRIS-Generator.git

cd Dynamic-QRIS-Generator
python -m venv <venv name>
pip install -r requirements.txt
```
## How to Use
### Edit `main.py` file
Edit these line. Get QRIS string from OCR like google lens or else
```python
#QRCode
STATIC_QRIS = ""
#default output folder
Save_Folder = "./output"
```
### Run the program
```bash
python main.py <amount>
```
Image output stored in `output` folder for default

## Example
```console
$ python main.py 5000
Generating Dynamic QRIS for Rp 5000...

New QRIS String:
00020101021226610016ID.CO.SHOPEE.WWW01189360091800229523010208229523010303UMI51440014ID.CO.QRIS.WWW0215ID10265078185930303UMI5204581753033605802ID5911Vyson Store6010TRENGGALEK61056636162070703A01540450006304281F

Success! QR code saved as qris_5000.png
```

## Output
you can also scan it :3
![QRIS Image](https://user17133.na.imgto.link/public/20260720/qris-5000.avif)


## Next Feature (soon)

