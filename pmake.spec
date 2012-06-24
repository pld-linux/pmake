Summary:	The BSD 4.4 version of make
Summary(de):	Berkeley's Parallel Make
Summary(fr):	Make parall�le de Berkeley
Summary(pl):	make w wersji z BSD 4.4
Summary(tr):	Paralel Make program�
Name:		pmake
Version:	2.1.36
Release:	2
License:	BSD
Group:		Development/Tools
Source0:	ftp://ftp.icsi.berkeley.edu/pub/ai/stolcke/software/%{name}-%{version}.tar.Z
# Source0-md5:	7831782071d2389849f81ed22b429edd
Source1:	%{name}-sys-alpha.mk
Source2:	%{name}-sys-i386.mk
Source3:	%{name}-sys-sparc.mk
Source4:	%{name}-sys-ppc.mk
Source5:	%{name}-sys-x86_64.mk
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-include.patch
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

%description -l de
Das Programm make dient zum Koordinieren der Kompilierung und
Verkn�pfen einer Reihe von Quellen zu einem Programm, wobei nur die
notwendigen Teile neu kompiliert werden, was dem. Entwickler viel Zeit
spart. make kann noch viel mehr- lesen Sie die Doku.

Pmake ist eine besondere Version von make, die zus�tzliche Syntax
unterst�tzt, die im herk�mmlichen Programm nicht enthalten ist. Einige
Berkeley-Programme enthalten Makefiles f�r pmake.

%description -l fr
make sert � coordonner la compilation et l'�dition de liens d'un
ensemble de sources pour donner un programme, en ne recompilant que ce
qui est n�cessaire et en faisant donc gagner beaucoup de temps au
d�veloppeur. En fait, make peut faire beaucoup plus, lisez les docs
info.

pmake est une version particuli�re de make qui g�re une syntaxe
additionnelle qui n'est pas dans le make standard. Certains programmes
Berkeley ont des makefiles �crits pour pmake.

%description -l pl
make jest narz�dziem GNU pozwalaj�cym na budowanie i instalowanie
program�w bez wi�kszej wiedzy na temat procesu budowania. Szczeg�y
dotycz�ce tego jak program powinien by� budowany s� do��czane do
Makefile programu. pmake jest konkretn� wersj� (BSD 4.4) make. pmake
obs�uguje troch� rozszerze� sk�adni, kt�rych nie ma standardowy make.
Niekt�re programy z BSD maj� Makefile pisane dla pmake.

%description -l tr
Pmake, standart make program� i�inde yer almayan ek bir tak�m
s�zdizimlerini destekleyen bir make program s�r�m�d�r. Baz� Berkeley
programlar�, pmake i�in yaz�lm�� Makefile dosyalar�na sahiptir.

%package customs
Summary:	A remote execution facility for pmake
Summary(pl):	U�atwienie zdalnego wywo�ywania pmake
Group:		Development/Tools

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

%description customs -l pl
customs to dodatek do pmake u�atwiaj�cy zdalne uruchamianie. customs
jest zaprojektowany do pracy na maszynach w sieci ze sp�jnym,
dzielonym systemem plik�w. Wymaga Sun RPC aby u�ywa� procedur XDR
(eXternal Data Representation) do logowania funkcji.

Pojedynczy serwer jest wyznaczany jako g��wny i jest dodatkowo
odpowiedzialny za sprawdzenie kiedy inna maszyna przestaje dzia�a� (z
kt�rej to maszyny dowolna inna maszyna musi przej�� prace), oraz za
przydzia� dost�pnych maszyn ��daj�cych ich klientom. Praca g��wnego
serwera nie jest oddawania jednej maszynie, ale raczej jest
przydzielana wybranej spo�r�d aktywnych kiedy poprzednia przestaje
dzia�a�.

Klienci maj� z zadanie:
- podawa� kryteria swojej dost�pno�ci (importquota)
- sprawdza� stan wszystkich zarejestrowanych maszyn w sieci (reginfo)
- zako�czy�, zrestartowa�, pingowa� dowolnego agenta customs (cctrl)
- wyda� polecenie z pow�oki (export)
- przyj�� logi od innych maszyn w sieci (logd).

%prep
%setup -q -n pmake
%patch0 -p1
%patch1 -p1

for I in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
	cp -f $I ./lib/mk/`echo $I | sed 's@.*sys-@sys-@'`
done
for I in i486 i586 i686 i786 athlon; do
	ln -sf sys-i386.mk lib/mk/sys-$I.mk
done
for I in sparc64 sparcv9; do
	ln -sf sys-sparc.mk lib/mk/sys-$I.mk
done

for I in makefile config.mk common.mk doc/Makefile ; do
  perl -pi -e '
    s,= /usr/local/bin,= %{_bindir},;
    s,= /usr/local/lib/pmake,= %{_datadir}/pmake,;
    s,= /usr/bin,= %{_bindir},;
    s,= /usr/sbin,= %{_sbindir},;
    s,= /usr/lib/pmake,= %{_datadir}/pmake,;
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
%{__make} CC="%{__cc} %{rpmcflags}" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake
%{__make} CC="%{__cc} %{rpmcflags}" SYSFLAGS="-DSYSV -DSVR4" \
	BINDIR=`pwd`/bin LIBDIR=`pwd`/lib/pmake install

#
# Then build pmake using pmake & Makefile's
`pwd`/bin/pmake CC="%{__cc} %{rpmcflags}" SYSFLAGS="-DSYSV -DSVR4" \
	ETCDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_datadir}/pmake \
	USRLIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir}/customs \
        all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_includedir},%{_libdir},%{_mandir}}

`pwd`/bin/pmake CC="%{__cc} %{rpmcflags}" SYSFLAGS="-DSYSV -DSVR4" \
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc customs/README.customs CHANGES README doc/* etc tests
%attr(755,root,root) %{_bindir}/pmake
%attr(755,root,root) %{_bindir}/vmake
%{_mandir}/man1/pmake.1*
%{_datadir}/pmake

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
