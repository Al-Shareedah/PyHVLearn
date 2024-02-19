from OpenSSL import crypto
import os
from datetime import datetime


class CertificateTemplate:
    ID_TYPE_NONE = 0  # Common name
    ID_TYPE_DNS = 1  # DNS
    ID_TYPE_IPADDR = 2  # IP ADDRESS
    ID_TYPE_EMAIL = 3  # EMAIL

    def __init__(self, name, idType=ID_TYPE_NONE):
        self.keyFile = None
        self.certFile = None
        self.name = name
        self.idType = idType
        self.tempPath = os.path.join(os.getenv('TMPDIR', '/tmp'))
        self.do_setup()

    def do_setup(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        cert_file_name = f"cert-{timestamp}.pem"
        key_file_name = f"cert-{timestamp}.key"

        self.certFile = os.path.join(self.tempPath, cert_file_name)
        self.keyFile = os.path.join(self.tempPath, key_file_name)

        self.write_cert()

    def get_cert_file_name(self):
        return self.certFile

    def get_key_file_name(self):
        return self.keyFile

    def write_cert(self):
        cname = self.name
        # Generate certificate and key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        # CommonName (CN) is set here; ensure it matches the hostname you will verify.
        cert.get_subject().CN = cname
        cert.set_serial_number(int(datetime.now().timestamp()))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)  # 10 years
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)

        # Add subjectAltName extension
        san_list = []
        if self.idType == self.ID_TYPE_DNS:
            san_list.append("DNS:" + self.name)
        elif self.idType == self.ID_TYPE_IPADDR:
            san_list.append("IP:" + self.name)
        elif self.idType == self.ID_TYPE_EMAIL:
            san_list.append("email:" + self.name)
        else:
            # Fallback to DNS if no specific type is found, adjust as necessary.
            san_list.append("DNS:" + self.name)

        # Convert the SAN list to a comma-separated string.
        san_str = ", ".join(san_list)
        # Creating an X509 extension for subjectAltName
        san_extension = crypto.X509Extension(b"subjectAltName", False, san_str.encode('utf-8'))
        cert.add_extensions([san_extension])

        cert.sign(key, 'sha256')

        # Write to files
        with open(self.certFile, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(self.keyFile, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

