from CertificateTemplate import CertificateTemplate
from Verifier import Verifier
from DFAInfer import DFAInfer

if __name__ == "__main__":
    # Create a certificate for example.com
    alphabet_file_path = "example-inputs/alphabets"
    name_file_path = "example-inputs/certname"
    name = "example.com"

    # ID type is set to EMAIL for demonstration, matching your Python example
    id_type = CertificateTemplate.ID_TYPE_EMAIL  # Adjust as per your needs
    cert_template = CertificateTemplate(name, id_type)
    cert_file = cert_template.get_cert_file_name()

    # Initialize Verifier and verify the certificate
    verifier = Verifier(name)
    verifier.read_cert(cert_file)
    # Declare dfaTest instance of DFACertname class
    dfaTest = DFAInfer()
    dfaTest.setAlphabetFile(alphabet_file_path)  # Set the alphabet file here
    dfaTest.setNameFile(name_file_path)  # Set the name file path
    dfaTest.setIdentityVerifier(verifier)
    dfaTest.setIdType(id_type)

    dfaTest.do_setup()

    # Adjust the query based on idType, using EMAIL as an example
    result = verifier.verify_name(f"email:{name}", "CN")  # Adjust the query string based on idType
    print(f"Verification result: {result}")



    # Assuming there's a cleanup or free method in your Verifier class
    verifier.free_cert()
