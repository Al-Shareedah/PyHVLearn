size_t jcstring(const char *name, size_t namelen, char *out)
{
    unsigned int i = 0;
    unsigned int j = 0;

    memset(out, 0, namelen+1);

    for (i = 0; i < namelen; i++) {
        /* Check for NULL character */
        if ((i+1) <  namelen) {
            if (name[i] == (char)0xC0 && name[i+1] == (char)0x80) {
                out[j] = '\0';
                i++;
                j++;
                continue;
            }
            if (name[i] == (char)0xCE && name[i+1] == (char)0xB5
                    && namelen == 2) {
                /* empty string ε */
                return 0;
            }
        }

        out[j] = name[i];
        j++;

    }

    out[j] = '\0';
    return j; /* string length */

}