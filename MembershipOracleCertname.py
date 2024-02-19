import ssl
from OpenSSL import crypto
import os

import CertificateTemplate
from Verifier import Verifier


class MembershipOracleCertname:
    def __init__(self, name, id_type):

        self.id_type = id_type
        self.name = name
        self.cert_file_name = None
        self.key_file_name = None
        self.do_setup()

    def do_setup(self):
        from CertificateTemplate import CertificateTemplate
        try:
            cert_template = CertificateTemplate(self.name, self.id_type)
            self.cert_file_name = cert_template.get_cert_file_name()
            self.key_file_name = cert_template.get_key_file_name()
        except RuntimeError as e:
            print(f"[FAILED] {str(e)}")
            exit(-1)

    def verify_certificate(self, hostname):
        """
        Verify if the generated certificate matches the provided hostname.
        """
        # Load the certificate
        with open(self.cert_file_name, 'rb') as cert_file:
            cert_data = cert_file.read()

        # Load the certificate using OpenSSL
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

        # Convert the certificate to the format required by match_hostname
        san_items = []
        for i in range(certificate.get_extension_count()):
            ext = certificate.get_extension(i)
            if 'subjectAltName' in str(ext.get_short_name()):
                # Decode the extension's data
                ext_data = str(ext)
                # Split the extension's data by comma and then by colon
                for alt_name in ext_data.split(", "):
                    parts = alt_name.split(":")
                    if len(parts) == 2:
                        san_items.append((parts[0], parts[1]))

        cert_dict['subjectAltName'] = san_items

        # Perform the hostname verification
        try:
            ssl.match_hostname(cert_dict, hostname)
            return True
        except ssl.CertificateError as e:
            print(f"Certificate verification failed: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":

    oracle = MembershipOracleCertname("a.a", 0)
    hostname_to_verify = "a.a"
    oracle.verify_certificate(hostname_to_verify)