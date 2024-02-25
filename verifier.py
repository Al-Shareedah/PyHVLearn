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


class JNIVerifier:
    def __init__(self, name):
        self.name = name

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
    cert_template = CertificateTemplate("example.com", CertificateTemplate.ID_TYPE_DNS)
    print(f"Certificate generated at: {cert_template.cert_file}")
    print(f"Key generated at: {cert_template.key_file}")

    # Example usage of JNIVerifier to read and verify a certificate
    verifier = JNIVerifier("exampleVerifier")

    try:
        print("Reading certificate...")
        verifier.read_cert(cert_template.cert_file, cert_template.key_file)
        print("Certificate read successfully.")

        # Suppose we want to verify the name "example.com" against the certificate
        print("Verifying certificate...")
        verification_result = verifier.verify("example.com", CertificateTemplate.ID_TYPE_DNS)

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
