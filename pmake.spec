Summary:	The BSD 4.4 version of make.
Name:		pmake
Version:	2.1.34
Release:	6
License:	BSD
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
Source0:	ftp://ftp.icsi.berkeley.edu/pub/ai/stolcke/software/%{name}-%{version}.tar.Z
Source1:	pmake-sys-alpha.mk
Source2:	pmake-sys-i386.mk
Source3:	pmake-sys-sparc.mk
Patch0:		pmake-glibc.patch
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
%patch0 -p1

for I in alpha i386 sparc; do
	cp -f $RPM_SOURCE_DIR/pmake-sys-$I.mk ./lib/mk/sys-$I.mk
done
for I in i486 i586 i786; do
	ln -s sys-i386.mk lib/mk/sys-$I.mk
done
for I in sparc64 sparcv9; do
	ln -s sys-sparc.mk lib/mk/sys-$I.mk
done

for I in makefile config.mk common.mk doc/Makefile                              
do                                                                              
  perl -pi -e '
    s,= /usr/local/bin,= %{_bindir},;
    s,= /usr/local/lib/pmake,= %{_datadir}/mk,;
    s,= /usr/bin,= %{_bindir},;
    s,= /usr/sbin,= %{_sbindir},;
    s,= /usr/lib/pmake,= %{_datadir}/mk,;
    s,= /usr/lib,= %{_libdir},;
    s,= /usr/include,= %{_includedir},;
    s,/usr/man,%{_mandir},;
    s,/usr/lib/tmac,= %{_datadir}/tmac,
    ' $I
done                                                                            

%build
#
# Bootstrap build of local pmake with makefile's
mkdir bin
make	CC="gcc $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake
make	CC="gcc $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake install

#
# Then build pmake using pmake & Makefile's
`pwd`/bin/pmake CC="gcc $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
    ETCDIR=%{_sbindir} \
    MANDIR=%{_mandir} \
    LIBDIR=%{_datadir}/pmake \
    USRLIBDIR=%{_libdir} \
    INCLUDEDIR=%{_includedir}/customs \
        all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}%{_includedir},%{_libdir},%{_mandir}}

`pwd`/bin/pmake CC="gcc $RPM_OPT_FLAGS" SYSFLAGS="-DSYSV -DSVR4" \
    DESTDIR=${RPM_BUILD_ROOT} \
    ETCDIR=${RPM_BUILD_ROOT}%{_sbindir} \
    MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
    LIBDIR=${RPM_BUILD_ROOT}%{_datadir}/pmake \
    USRLIBDIR=${RPM_BUILD_ROOT}%{_libdir} \
    INCLUDEDIR=${RPM_BUILD_ROOT}%{_includedir}/customs \
        install

# XXX rename export.1 to customs_export.1 to avoid conflict with bash export.1.
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/{export,customs_export}.1
mv -f customs/README customs/README.customs

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	customs/README.customs CHANGES README \
	doc/tutorial.* doc/prefix.*


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz customs/*.gz doc/* etc tests
%attr(755,root,root) %{_bindir}/pmake
%attr(755,root,root) %{_bindir}/vmake
%{_mandir}/man1/pmake.1*
%{_libdir}/pmake

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
%{_mandir}/man1/customs_export.1*
%{_mandir}/man1/rexport.1*
%{_mandir}/man8/customs.8*
%{_mandir}/man8/cctrl.8*
%{_mandir}/man8/importquota.8*
%{_mandir}/man8/logd.8*

%attr(755,root,root) %{_libdir}/libcustoms*
%{_includedir}/customs
