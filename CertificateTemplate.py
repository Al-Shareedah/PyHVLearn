from ctypes import CDLL, c_char_p, c_int
import os
import time
import tempfile

class CertificateTemplate:
    ID_TYPE_NONE = 0  # Common name
    ID_TYPE_DNS = 1   # DNS
    ID_TYPE_IPADDR = 2  # IP ADDRESS
    ID_TYPE_EMAIL = 3  # EMAIL

    def __init__(self, name, id_type):
        self.id_type = id_type
        # Adjust the name based on the id_type
        self.name = self._adjust_name_based_on_id_type(name).encode('utf-8')
        self.lib = CDLL('/Users/al.halshareedah/Documents/GitHub/PyHVLearn/gnutls/libserverjni.so')
        self._setup_ctypes()
        self.cert_file = None
        self.key_file = None
        self.do_setup()

    def _adjust_name_based_on_id_type(self, name):
        if self.id_type == self.ID_TYPE_DNS:
            cname = "DNS:" + name
        elif self.id_type == self.ID_TYPE_IPADDR:
            cname = "IP:" + name
        elif self.id_type == self.ID_TYPE_EMAIL:
            cname = "email:" + name
        else:
            cname = name  # No prefix for ID_TYPE_NONE
        return cname

    def _setup_ctypes(self):
        # Setup argument and result types for ctypes calls
        self.lib.initcert.argtypes = [c_char_p, c_char_p, c_char_p]
        self.lib.initcert.restype = c_int

    def do_setup(self):
        # Generate filenames based on the current timestamp
        temp_path = tempfile.gettempdir()
        id_file = str(int(time.time()))
        cert_file_name = "cert-" + id_file + ".pem"
        key_file_name = "key-" + id_file + ".key"

        self.cert_file = os.path.join(temp_path, cert_file_name)
        self.key_file = os.path.join(temp_path, key_file_name)

        # Generate the certificate
        result = self.lib.initcert(self.name, self.cert_file.encode('utf-8'), self.key_file.encode('utf-8'))
        if result != 0:
            raise Exception("Failed to generate certificate")

    def get_cert_file_name(self):
        return self.cert_file

    def get_key_file_name(self):
        return self.key_file

# Example usage
if __name__ == "__main__":
    certificate_template_dns = CertificateTemplate("example.com", CertificateTemplate.ID_TYPE_DNS)
    print("DNS Certificate file:", certificate_template_dns.get_cert_file_name())
    print("DNS Key file:", certificate_template_dns.get_key_file_name())

    certificate_template_email = CertificateTemplate("user@example.com", CertificateTemplate.ID_TYPE_EMAIL)
    print("Email Certificate file:", certificate_template_email.get_cert_file_name())
    print("Email Key file:", certificate_template_email.get_key_file_name())
