#
# These are the variables used to specify the nature of the system on which
# pmake is running. These names may later be used in #if expressions for
# conditional reading of the enclosed portion of the Makefile
#

sparc=   Machine is a sparc

linux=   running linux
SYSV=    This is not only System 5 
SVR4=    but even Release 4 compatible
unix=	 It runs UNIX.

# some non-standard locations
CC = /usr/bin/cc
AS = /usr/bin/as
AR = /usr/bin/ar
LD = /usr/bin/ld
LINT = :

