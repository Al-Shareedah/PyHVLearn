from typing import List, Callable
from CertificateTemplate import CertificateTemplate
import os


# Assuming Verifier and CertificateTemplate classes are defined as provided

class MembershipOracleHostname:
    def __init__(self, verifier, name, id_type):
        self.verifier = verifier
        self.name = name
        self.id_type = id_type

    def process_queries(self, queries: List[str], answer_callback: Callable[[str, bool], None]):
        for qstr in queries:
            try:
                # Use CertificateTemplate to create a certificate for the query
                cert_template = CertificateTemplate(qstr, self.id_type)
                cert_file_name = cert_template.get_cert_file_name()

                # Read the certificate using the verifier
                self.verifier.read_cert(cert_file_name)

                # Verify the name using the verifier
                accepted = self.verifier.verify_name(self.name, "CN")  # Simplified assumption for id_type

            except Exception as e:
                print(f"[FAILED] {e}")
                answer_callback(qstr, False)
                continue
            finally:
                # Free the certificate (dereference)
                self.verifier.free_cert()
                # Optionally, delete the generated certificate and key files
                os.remove(cert_file_name)
                os.remove(cert_template.get_key_file_name())

            print(f"query: {qstr} >> ", end="")
            if accepted:
                print("[accepted]")
                answer_callback(qstr, True)
            else:
                print("[rejected]")
                answer_callback(qstr, False)

# The Verifier class and CertificateTemplate class remain as previously defined
