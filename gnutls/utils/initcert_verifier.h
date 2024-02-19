// In a new or existing header file, replacing jni_initcert.h and jni_verifier.h
#ifndef SERVER_FUNCTIONS_H
#define SERVER_FUNCTIONS_H

int initcert(const char *commonname, const char *crtfile, const char *keyfile);
int readcert(const char *crtfile);
void freecert(void);
int verifyname(const char *hostname, int id);

#endif // SERVER_FUNCTIONS_H
