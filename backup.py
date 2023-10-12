import requests
import smtplib
from email.message import EmailMessage
import json

# Membaca daftar URL dari conf.json
with open("conf.json", "r") as file:
    config_data = json.load(file)
    daftar_url = config_data.get("daftar_url", [])
    smtp_server = config_data.get('email', {}).get('smtp_server', '')
    stmp_port = config_data.get('email', {}).get('stmp_port', '')
    email_address = config_data.get('email', {}).get('email_address', '')
    email_password = config_data.get('email', {}).get('email_password', '')
    recipient_addresses = config_data.get('email', {}).get('recipient_addresses', '')


# Melakukan looping untuk mengakses URL
for url in daftar_url:
    try:
        response = requests.get(url)
        # Periksa kode status HTTP untuk menentukan apakah permintaan berhasil
        if response.status_code < 200 and response.status_code > 299:
            pesan = f"Situs web {url} tidak dapat diakses. Status code: {response.status_code}"

            # Mengirim notifikasi email menggunakan SMTP
            try:
                server = smtplib.SMTP(smtp_server, stmp_port)  # Server SMTP dan port
                server.starttls()  # Mengenkripsi koneksi
                server.login(email_address, email_password)  # Login ke email pengirim
                msg = f"Subject: Notifikasi Situs Web Tidak Dapat Diakses\n\n{pesan}"
                server.sendmail(email_address, recipient_addresses, msg)  # Mengirim pesan email
                server.quit()  # Keluar dari server
                print("Notifikasi email telah dikirim.")
            except Exception as e:
                print(f"Gagal mengirim email: {e}")
            else:
                print(f"Berhasil mengakses URL: {url}")

    except Exception as e:
        print(f"Gagal mengakses URL: {url}, Error: {str(e)}")