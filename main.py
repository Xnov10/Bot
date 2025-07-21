import qrcode

# Data for the QR Code
data = 'Standar Pembayaran Nasional WAN STORE NMID: ID1024326770533 Dicetak oleh: 93600914 A01 SATU QRIS UNTUK SEMUA Cek aplikasi penyelenggara di: www.aspi-qris.id Versi cetak: V1.O.2024.08.06 GPN Cara pembayaran QRIS Buka Aplikasi scan dan cek Bayar Berlogo QRIS'

# Generate QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code
img = qr.make_image(fill_color='black', back_color='white')
img.save('qrcode.png')
