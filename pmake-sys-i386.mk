#
# These are the variables used to specify the nature of the system on which
# pmake is running. These names may later be used in #if expressions for
# conditional reading of the enclosed portion of the Makefile
#

i386=    Machine should be compatable with a i386
i486=    Machine should be compatable with a i386
i586=    Machine should be compatable with a i386
i686=    Machine should be compatable with a i386

LIN != /bin/uname -s
#if $(LIN) == "Linux"
linux=   running linux
SYSV=    This is not only System 5 
SVR4=    but even Release 4 compatible
#else
bsdi=    running BSDI
#endif
unix=	 It runs UNIX.

# some non-standard locations
CC = /usr/bin/cc
AS = /usr/bin/as
AR = /usr/bin/ar
LD = /usr/bin/ld
LINT = :

