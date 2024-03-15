import ctypes
import os
from ctypes import c_char_p, c_int
import tempfile
import time
from CertificateTemplate import CertificateTemplate

# Load the shared library
lib_path = '/Users/al.halshareedah/Documents/GitHub/PyHVLearn/gnutls/libserverjni.so'
lib = ctypes.CDLL(lib_path)

# Define argument and result types for the C functions if needed
lib.initcert.argtypes = [c_char_p, c_char_p, c_char_p]
lib.initcert.restype = c_int

lib.readcert.argtypes = [c_char_p]
lib.readcert.restype = c_int

lib.freecert.argtypes = []
lib.freecert.restype = None

lib.verifyname.argtypes = [c_char_p, c_int]
lib.verifyname.restype = c_int


class Verifier:
    def __init__(self, id_type):
        self.id_type = id_type

    def read_cert(self, crt_file, key_file):
        # Ignore key_file in this method
        result = lib.readcert(crt_file.encode('utf-8'))
        if result != 0:
            raise IOError("Failed to read certificate")

    def verify(self, qstr, id_type):
        return lib.verifyname(qstr.encode('utf-8'), id_type)

    def free_cert(self):
        lib.freecert()


def main():
    # Example usage of CertificateTemplate to generate a certificate
    print("Generating certificate...")
    cert_template = CertificateTemplate("*.a.a", CertificateTemplate.ID_TYPE_DNS)  # This part remains unchanged as it's just an example of generating a certificate
    print(f"Certificate generated at: {cert_template.cert_file}")
    print(f"Key generated at: {cert_template.key_file}")

    # Example usage of Verifier to read and verify a certificate
    verifier = Verifier(0)  # Assuming 0 represents the equivalent of ID_NONE in your shared library

    try:
        print("Reading certificate...")
        verifier.read_cert(cert_template.cert_file, cert_template.key_file)  # You still need a valid certificate file path
        print("Certificate read successfully.")

        # Now, verify the hostname ".a.A" against the certificate
        print("Verifying certificate for hostname '.a.A'...")
        verification_result = verifier.verify(".a.A", 0)  # Assuming 0 is the correct id_type for your use case

        if verification_result == 1:
            print("Verification successful.")
        else:
            print("Verification failed.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Cleaning up...")
        verifier.free_cert()


if __name__ == "__main__":
    main()
