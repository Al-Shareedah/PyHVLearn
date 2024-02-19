from OpenSSL import crypto


class Verifier:
    ID_TYPE_NONE = 0  # Common name
    ID_TYPE_DNS = 1  # DNS
    ID_TYPE_IPADDR = 2  # IP Address
    ID_TYPE_EMAIL = 3  # Email

    def __init__(self, name):
        self.certificate = None
        self.name = name

    def read_cert(self, crt_file):
        with open(crt_file, "rb") as file:
            crt_data = file.read()
            self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, crt_data)

    def verify_name(self, qstr, idType):
        if self.certificate is None:
            raise ValueError("Certificate not loaded.")

        verified = False
        if idType == self.ID_TYPE_NONE:  # Common Name
            subject = self.certificate.get_subject()
            cn = subject.CN
            verified = cn == qstr
        elif idType == self.ID_TYPE_DNS:  # DNS
            ext_count = self.certificate.get_extension_count()
            for i in range(ext_count):
                ext = self.certificate.get_extension(i)
                if 'subjectAltName' in str(ext.get_short_name()):
                    dns_names = str(ext).split(', ')
                    for dns in dns_names:
                        if dns.startswith('DNS:') and dns[4:] == qstr:
                            verified = True
                            break
        elif idType == self.ID_TYPE_IPADDR:  # IP Address
            ext_count = self.certificate.get_extension_count()
            for i in range(ext_count):
                ext = self.certificate.get_extension(i)
                if 'subjectAltName' in str(ext.get_short_name()):
                    ip_addresses = str(ext).split(', ')
                    for ip in ip_addresses:
                        if ip.startswith('IP Address:') and ip[11:] == qstr:
                            verified = True
                            break
        elif idType == self.ID_TYPE_EMAIL:  # Email
            subject = self.certificate.get_subject()
            email = getattr(subject, 'emailAddress', None)
            verified = email == qstr

        return verified

    def free_cert(self):
        self.certificate = None

    def getName(self):
        return self.name
