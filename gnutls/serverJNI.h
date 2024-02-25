
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <gnutls/x509.h>


extern gnutls_x509_crt_t crt;

#include "utils/dfa.h"
#include "gnutls/crt_gen.h"
// Function declarations
int readcert(const char *crtfile);
void freecert(void);
int verifyname(const char *hostname, int id);