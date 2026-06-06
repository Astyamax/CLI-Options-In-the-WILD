#include <errno.h>
#include <stdlib.h>

#ifndef ENODATA
#define ENODATA ENOENT
#endif

int getfilecon(const char *path, char **con)
{
    (void)path;
    if (con != NULL) {
        *con = NULL;
    }
    errno = ENODATA;
    return -1;
}

int lgetfilecon(const char *path, char **con)
{
    return getfilecon(path, con);
}

int fgetfilecon(int fd, char **con)
{
    (void)fd;
    if (con != NULL) {
        *con = NULL;
    }
    errno = ENODATA;
    return -1;
}

int getfilecon_raw(const char *path, char **con)
{
    return getfilecon(path, con);
}

int lgetfilecon_raw(const char *path, char **con)
{
    return getfilecon(path, con);
}

int fgetfilecon_raw(int fd, char **con)
{
    return fgetfilecon(fd, con);
}

void freecon(char *con)
{
    free(con);
}
