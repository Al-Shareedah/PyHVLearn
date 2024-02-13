from CertificateTemplate import CertificateTemplate
from Verifier import Verifier
from DFAInfer import DFAInfer

if __name__ == "__main__":
    # Create a certificate for example.com
    alphabet_file_path = "example-inputs/alphabets"
    name_file_path = "example-inputs/certname"


    # ID type is set to EMAIL for demonstration, matching your Python example
    id_type = CertificateTemplate.ID_TYPE_EMAIL  # Adjust as per your needs



    # Declare dfaTest instance of DFACertname class
    dfaTest = DFAInfer()
    dfaTest.setAlphabetFile(alphabet_file_path)  # Set the alphabet file here
    dfaTest.setNameFile(name_file_path)  # Set the name file path
    dfaTest.setIdType(id_type)

    dfaTest.do_setup()





