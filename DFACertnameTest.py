from CertificateTemplate import CertificateTemplate
from Verifier import Verifier
from DFAInfer import DFAInfer
from py4j.java_gateway import JavaGateway

if __name__ == "__main__":
    # Create a certificate for example.com
    alphabet_file_path = "example-inputs/alphabets"
    name_file_path = "example-inputs/certname"

    # ID type is set to EMAIL for demonstration, matching your Python example
    id_type = CertificateTemplate.ID_TYPE_EMAIL  # Adjust as per your needs

    # Declare dfaTest instance of DFACertname class
    dfaTest = DFAInfer(alphabet_file_path, name_file_path, id_type)
    dfaTest.do_setup()






