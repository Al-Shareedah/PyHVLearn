from OpenSSL import crypto


class Verifier:
    def __init__(self, name):
        self.certificate = None
        self.name = name

    def read_cert(self, crt_file):
        """
        Reads a certificate file and stores it in the instance.
        """
        with open(crt_file, "rb") as file:
            crt_data = file.read()
            self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, crt_data)

    def verify_name(self, qstr, id_type):
        """
        Verifies the name in the certificate.

        Parameters:
        - qstr: The string to verify against the certificate's subject.
        - id_type: The type of identifier to verify (e.g., common name, email).
                  For simplicity, this example will focus on common names.

        Returns:
        - True if the qstr matches the certificate's subject common name, False otherwise.
        """
        if self.certificate is None:
            raise ValueError("Certificate not loaded.")

        # Extract the subject from the certificate
        subject = self.certificate.get_subject()
        cn = subject.CN  # Common Name

        # Verify based on the id_type (simplified for this example)
        if id_type == "CN" and cn == qstr:
            return True
        else:
            return False

    def free_cert(self):
        """
        Frees resources associated with the certificate.
        In this context, it simply dereferences the certificate object.
        """
        self.certificate = None

    def getName(self):
        return self.name
