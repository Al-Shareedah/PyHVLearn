from CertificateTemplate import CertificateTemplate
from Verifier import Verifier

if __name__ == "__main__":
    # Create a certificate for example.com
    name = "example.com"
    id_type = CertificateTemplate.ID_TYPE_IPADDR  # For demonstration, assuming we're using EMAIL as ID type
    cert_template = CertificateTemplate(name, id_type)
    cert_file = cert_template.get_cert_file_name()

    # Output the location of the created certificate and key
    print(f"Certificate saved to: {cert_file}")
    print(f"Key saved to: {cert_template.get_key_file_name()}")

    # Verify the certificate's common name (CN) using PyOpenSSLVerifier
    verifier = Verifier(name)
    verifier.read_cert(cert_file)
    result = verifier.verify_name(f"email:{name}", "CN")  # Adjust the query string based on idType
    print(f"Verification result: {result}")

    verifier.free_cert()
