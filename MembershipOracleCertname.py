from ctypes import CDLL, c_char_p, c_int

# Load the shared library
libserverjni = CDLL('/Users/al.halshareedah/Documents/GitHub/PyHVLearn/gnutls/libserverjni.so')

# Define the argument and return types for the functions we'll call
libserverjni.initcert.argtypes = [c_char_p, c_char_p, c_char_p]
libserverjni.initcert.restype = c_int

libserverjni.readcert.argtypes = [c_char_p]
libserverjni.readcert.restype = c_int

libserverjni.verifyname.argtypes = [c_char_p, c_int]
libserverjni.verifyname.restype = c_int

libserverjni.freecert.argtypes = []
libserverjni.freecert.restype = None

# Example usage
def main():
    common_name = b"*.a.a"
    crt_file = b"/tmp/example_com.crt"
    key_file = b"/tmp/example_com.key"

    # Generate a certificate
    if libserverjni.initcert(common_name, crt_file, key_file) == 0:
        print("Certificate generated successfully.")
    else:
        print("Failed to generate certificate.")
        return

    # Read the generated certificate
    if libserverjni.readcert(crt_file) == 0:
        print("Certificate read successfully.")
    else:
        print("Failed to read certificate.")
        return

        # Verify the hostname against the loaded certificate
    ID_DNS = 0  # Assuming ID_DNS = 1 based on your setup
    verification_result = libserverjni.verifyname(common_name, ID_DNS)
    if verification_result == 1:
        print("Hostname verification: Accepted")
    elif verification_result == 0:
        print("Hostname verification: Rejected")
    else:
        print("Error during hostname verification.")

    # Clean up and free the certificate
    libserverjni.freecert()

if __name__ == "__main__":
    main()
