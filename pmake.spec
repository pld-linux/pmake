Summary:	The BSD 4.4 version of make.
Name:		pmake
Version:	2.1.33
Release:	5
License:	BSD
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
Source0:	ftp://ftp.icsi.berkeley.edu/pub/ai/stolcke/software/%{name}-%{version}.tar.Z
Source1:	pmake-sys-alpha.mk
Source2:	pmake-sys-i386.mk
Source3:	pmake-sys-sparc.mk
Patch0:		pmake-2.1.33-glibc.patch
Patch1:		pmake-2.1.33-compat21.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Make is a GNU tool which allows users to build and install programs
without any significant knowledge of the build process. Details about
how the program should be built are included in the program's
Makefile. Pmake is a particular version (BSD 4.4) of make. Pmake
supports some additional syntax which is not in the standard make
program. Some Berkeley programs have Makefiles written for pmake.

Pmake should be installed on your system so that you will be able to
build programs which require using pmake instead of make.

%package customs
Summary:	A remote execution facility for pmake.
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia

%description customs
Customs is a remote execution facility for PMake. Customs is designed
to run on a network of machines with a consistent, shared filesystem.
Customs requires Sun RPC in order to use XDR (eXternal Data
Representation) routines for logging functions.

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
install -d $RPM_BUILD_ROOT%{_prefix}/{bin,include,lib,man,sbin}

`pwd`/bin/pmake CC="egcs $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	DESTDIR=$RPM_BUILD_ROOT install

mv -f customs/README customs/README.customs

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	customs/README.customs CHANGES README \
	doc/tutorial.* doc/prefix.*


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pmake
%attr(755,root,root) %{_bindir}/vmake
%{_mandir}/man1/pmake.1*
%{_libdir}/pmake
%doc *.gz customs/*.gz doc/* etc tests

%files customs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/reginfo
%attr(755,root,root) %{_bindir}/export
%attr(755,root,root) %{_bindir}/rexport
%attr(755,root,root) %{_sbindir}/importquota
%attr(755,root,root) %{_sbindir}/cctrl
%attr(755,root,root) %{_sbindir}/logd
%attr(755,root,root) %{_sbindir}/customs

%{_mandir}/man1/reginfo.1*
%{_mandir}/man1/export.1*
%{_mandir}/man1/rexport.1*
%{_mandir}/man8/customs.8*
%{_mandir}/man8/cctrl.8*
%{_mandir}/man8/importquota.8*
%{_mandir}/man8/logd.8*

%attr(755,root,root) %{_libdir}/libcustoms*
%{_includedir}/customs
