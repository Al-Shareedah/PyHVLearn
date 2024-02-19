#ifndef DFA_H
#define DFA_H

#include "jcstring.h"
#include "initcert_verifier.h"

/* DFA return status */
#define ACCEPT  1
#define REJECT  0
#define ERROR   2

/* Define each matching identifier type: NONE, DNS, IP, EMAIL to test */
#define ID_NONE     0
#define ID_DNS      1
#define ID_IPADDR   2
#define ID_EMAIL    3

#endif // DFA_H
