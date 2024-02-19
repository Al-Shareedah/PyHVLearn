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

    if (id == ID_NONE || id == ID_DNS || id == ID_IPADDR) {
        ret = gnutls_x509_crt_check_hostname(crt, hostname) ? ACCEPT : REJECT;
    } else if (id == ID_EMAIL) {
        ret = gnutls_x509_crt_check_email(crt, hostname, 0) ? ACCEPT : REJECT;
    } else {
        fprintf(stderr, "[FAILED] verifyname() -- ID not found.\n");
    }

    return ret;
}
