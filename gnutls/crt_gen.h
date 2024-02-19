#include "crt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DUMMY "dummy-value"

// This function is now adapted to be called directly from C (or Python via ctypes)
int initcert(const char *commonname, const char *crtfile, const char *keyfile) {
    int ret;

    gnutls_x509_crt_t crt;
    gnutls_x509_privkey_t pkey;

    const char *cnamestr = commonname;
    size_t cnamelen = strlen(cnamestr);

    size_t buf_size;

    ret = 1;

    /* Generate private key */
    if (gnutls_gen_key(&pkey) != 0) {
        fprintf(stderr, "[FAILED] gnutls_gen_key().\n");
        return ret;
    }

    if (gnutls_gen_crt(&crt) != 0) {
        fprintf(stderr, "[FAILED] gnutls_gen_crt().\n");
        gnutls_x509_privkey_deinit(pkey);
        return ret;
    }

    /* Set name in common name or subject alternative name */
    char cname[cnamelen + 1];
    strncpy(cname, cnamestr, cnamelen);
    cname[cnamelen] = '\0'; // Ensure null termination

    if (gnutls_set_name(&crt, cname, cnamelen) != 0) {
        fprintf(stderr, "[FAILED] gnutls_set_name().\n");
        goto out;
    }

    ret = gnutls_x509_crt_get_dn_by_oid(crt, GNUTLS_OID_X520_COMMON_NAME,
            0, 1, NULL, &buf_size);
    //fprintf(stdout, "ret: %d data size: %lu\n", ret, buf_size);
    /* put dummy value in CN */
    if (ret == GNUTLS_E_REQUESTED_DATA_NOT_AVAILABLE) {
        if (gnutls_set_name(&crt, DUMMY, strlen(DUMMY)) != 0) {
            fprintf(stderr,
                    "[FAILED] gnutls_set_name(). -- cannot set dummy value\n");
            goto out;
        }
    }

    if (gnutls_sign_crt(&crt, &pkey) != 0) {
        fprintf(stderr, "[FAILED] gnutls_sign_crt().\n");
        goto out;
    }

    /* Write to disk */
    if (gnutls_write_crt(crt, crtfile) != 0) {
        fprintf(stderr, "[FAILED] gnutls_write_crt().\n");
        goto out;
    }

    if (gnutls_write_pkey(pkey, keyfile) != 0) {
        fprintf(stderr, "[FAILED] gnutls_write_pkey().\n");
        goto out;
    }

    ret = 0;

out:
    gnutls_x509_crt_deinit(crt);
    gnutls_x509_privkey_deinit(pkey);

    return ret;
}
