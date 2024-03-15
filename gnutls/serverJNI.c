#include "serverJNI.h"

// Removing the JNI-specific code and adapting it for direct C use.
gnutls_x509_crt_t crt;

// Adjusted function to read a certificate from a file.
int readcert(const char *crtfile) {
    int ret = 1; // Default to failure

    if (gnutls_read_crt(crtfile, &crt) != 0) {
        fprintf(stderr, "[FAILED] readcert()\n");
        return ret;
    }

    ret = 0; // Success
    return ret;
}

// Adjusted function to free the loaded certificate.
void freecert() {
    gnutls_x509_crt_deinit(crt);
}

// Adjusted function to verify a hostname or email against the loaded certificate.
int verifyname(const char *hostname, int id) {
    int ret = ERROR; // Default to error
    char processed_hostname[strlen(hostname) + 1];
     // Process the hostname using the C equivalent of jcstring and use the returned length
    size_t processed_hostname_len = c_jcstring(hostname, strlen(hostname), processed_hostname);

    if (id == ID_NONE || id == ID_DNS || id == ID_IPADDR) {
        ret = gnutls_x509_crt_check_hostname(crt, processed_hostname);
    } else if (id == ID_EMAIL) {
        ret = gnutls_x509_crt_check_email(crt, processed_hostname, 0);
    } else {
        fprintf(stderr, "[FAILED] verifyname() -- ID not found.\n");
    }

    return ret;
}
