#include <string.h> // For memset

size_t c_jcstring(const char *name, size_t namelen, char *out) {
    unsigned int i = 0;
    unsigned int j = 0;

    memset(out, 0, namelen + 1); // Initialize output buffer with zeros

    for (i = 0; i < namelen; i++) {
        if ((i+1) <  namelen) {
            if (name[i] == (char)0xC0 && name[i+1] == (char)0x80) {
                out[j] = '\0';
                i++; // Skip the next byte
                j++; 
                continue;
            }
        }
        out[j] = name[i];
        j++;
    }
    out[j] = '\0'; 
    return j; 
}
