Summary: The BSD 4.4 version of make.
Name: pmake
Version: 2.1.33
Release: 5
Copyright: BSD
Group: Development/Tools
Source0: ftp://ftp.icsi.berkeley.edu/pub/ai/stolcke/software/pmake-2.1.33.tar.Z
Source1: pmake-sys-alpha.mk
Source2: pmake-sys-i386.mk
Source3: pmake-sys-sparc.mk
Patch0: pmake-2.1.33-glibc.patch
Patch1: pmake-2.1.33-compat21.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Make is a GNU tool which allows users to build and install programs
without any significant knowledge of the build process.  Details
about how the program should be built are included in the program's
Makefile.  Pmake is a particular version (BSD 4.4) of make.  Pmake
supports some additional syntax which is not in the standard make
program.  Some Berkeley programs have Makefiles written for pmake.

Pmake should be installed on your system so that you will be able to
build programs which require using pmake instead of make.

%package customs
Summary: A remote execution facility for pmake.
Group: Development/Tools

%description customs
Customs is a remote execution facility for PMake. Customs is designed to
run on a network of machines with a consistent, shared filesystem. Customs
requires Sun RPC in order to use XDR (eXternal Data Representation) routines
for logging functions.

A single server is designated as the master agent and is additionally
responsible for noting when a machine goes down, from which machines
any given machine will accept jobs and parcelling out available
machines to requesting clients. The job of master is not given to any
one machine but, rather, is decided among the active agents whenever
the previous master dies.

Clients are provided to:
	- alter the availability criteria for the local machine (importquota)
	- find the status of all registered hosts on the net (reginfo).
	- abort, restart or ping any customs agent on the network (cctrl).
	- export a command from the shell (export).
	- accept log information from all hosts on the net (logd).

%prep
%setup -q -n pmake
%patch0 -p1 -b .glibc
%patch1 -p1 -b .compat21

cp $RPM_SOURCE_DIR/pmake-sys-${RPM_ARCH}.mk ./lib/mk/sys-%{_arch}.mk

%build
#
# Bootstrap build of local pmake with makefile's
mkdir bin
make	CC="egcs $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake
make	CC="egcs $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake install

#
# Then build pmake using pmake & Makefile's
`pwd`/bin/pmake CC="egcs $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,include,lib,man,sbin}

`pwd`/bin/pmake CC="egcs $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	DESTDIR=$RPM_BUILD_ROOT install

mv -f customs/README customs/README.customs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,root)	/usr/bin/pmake
/usr/bin/vmake
/usr/man/man1/pmake.1
/usr/lib/pmake
%doc CHANGES INSTALL README customs/README.customs etc tests
%doc doc/tutorial.* doc/prefix.*

%files customs
%defattr(-,root,root)
/usr/bin/reginfo
%attr(755,root,root)	/usr/bin/export
/usr/bin/rexport
/usr/sbin/importquota
/usr/sbin/cctrl
/usr/sbin/logd
/usr/sbin/customs

/usr/man/man1/reginfo.1
/usr/man/man1/export.1
/usr/man/man1/rexport.1
/usr/man/man8/customs.8
/usr/man/man8/cctrl.8
/usr/man/man8/importquota.8
/usr/man/man8/logd.8

/usr/lib/libcustoms*
/usr/include/customs
