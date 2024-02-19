import ctypes
import os
from ctypes import c_char_p, c_int
import tempfile
import time

# Load the shared library
lib_path = "/Users/al.halshareedah/Documents/GitHub/HVLearn/ssl/gnutls/libserverJNI.so"
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


class CertificateTemplate:
    ID_TYPE_NONE = 0
    ID_TYPE_DNS = 1
    ID_TYPE_IPADDR = 2
    ID_TYPE_EMAIL = 3

    def __init__(self, name, id_type):
        self.id_type = id_type
        self.name = name
        self.do_setup()

    def do_setup(self):
        temp_path = tempfile.gettempdir()
        id_file = str(int(time.time()))

        cert_file_name = f"cert-{id_file}.pem"
        key_file_name = f"key-{id_file}.key"

        self.cert_file = os.path.join(temp_path, cert_file_name)
        self.key_file = os.path.join(temp_path, key_file_name)

        self.write_cert()

    def write_cert(self):
        cname = self.name
        if self.id_type == self.ID_TYPE_DNS:
            cname = f"DNS:{self.name}"
        elif self.id_type == self.ID_TYPE_IPADDR:
            cname = f"IP:{self.name}"
        elif self.id_type == self.ID_TYPE_EMAIL:
            cname = f"email:{self.name}"

        ret = lib.initcert(cname.encode('utf-8'),
                           self.cert_file.encode('utf-8'),
                           self.key_file.encode('utf-8'))
        if ret != 1:
            raise RuntimeError(f"certificate generation failed for {cname}")


class JNIVerifier:
    def __init__(self, name):
        self.name = name

    def read_cert(self, crt_file, key_file):
        # Ignore key_file in this method
        result = lib.readcert(crt_file.encode('utf-8'))
        if result != 1:
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
