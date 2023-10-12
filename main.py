from config import config
import requests
import smtplib
from email.message import EmailMessage

# Daftar URL dari konfigurasi
webs = config.config["webs"]

# Inisialisasi variabel untuk melacak kesalahan
errors = []

# Loop melalui setiap web dan URL
for web, urls in webs.items():
    for url in urls:
        response = requests.get(url)

        # Periksa status kode HTTP
        if response.status_code < 200 and response.status_code > 299:
            errors.append(f"URL {url} mengembalikan kode status {response.status_code}")

# Jika ada kesalahan, mengirim satu notifikasi email
if errors:
    email_config = config.config["email"]
    smtp_server = email_config["smtp_server"]
    smtp_port = email_config["smtp_port"]
    email_address = email_config["email_address"]
    email_password = email_config["email_password"]
    recipient_addresses = email_config["recipient_addresses"]

    message = EmailMessage()
    message.set_content("\n".join(errors))

    message["Subject"] = "Notifikasi Kesalahan URL"
    message["From"] = email_address
    message["To"] = recipient_addresses

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(message)
        server.quit()
        print("Notifikasi email telah dikirim.")
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
else:
    print(f"Berhasil mengakses URL: {url}")