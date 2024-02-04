from OpenSSL import crypto
import os
from datetime import datetime, timedelta

class CertificateTemplate:
    ID_TYPE_NONE = 0  # Common name
    ID_TYPE_DNS = 1  # DNS
    ID_TYPE_IPADDR = 2  # IP ADDRESS
    ID_TYPE_EMAIL = 3  # EMAIL

    def __init__(self, name, idType=ID_TYPE_NONE):
        self.name = name
        self.idType = idType
        self.tempPath = os.path.join(os.getenv('TMPDIR', '/tmp'))
        self.do_setup()

    def do_setup(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        certFileName = f"cert-{timestamp}.pem"
        keyFileName = f"cert-{timestamp}.key"

        self.certFile = os.path.join(self.tempPath, certFileName)
        self.keyFile = os.path.join(self.tempPath, keyFileName)

        self.write_cert()

    def get_cert_file_name(self):
        return self.certFile

    def get_key_file_name(self):
        return self.keyFile

    def write_cert(self):
        cname = self.name
        # Modify CN based on idType
        if self.idType == self.ID_TYPE_DNS:
            cname = f"DNS:{self.name}"
        elif self.idType == self.ID_TYPE_IPADDR:
            cname = f"IP:{self.name}"
        elif self.idType == self.ID_TYPE_EMAIL:
            cname = f"email:{self.name}"

        # Generate certificate and key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.get_subject().CN = cname
        cert.set_serial_number(int(datetime.now().timestamp()))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha256')

        # Write to files
        with open(self.certFile, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(self.keyFile, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

# Example usage
if __name__ == "__main__":
    name = "example.com"
    cert_template = CertificateTemplate(name, CertificateTemplate.ID_TYPE_EMAIL)
    print(f"Certificate saved to: {cert_template.get_cert_file_name()}")
    print(f"Key saved to: {cert_template.get_key_file_name()}")
    print(f"The type of ID is the following: {cert_template.idType}")