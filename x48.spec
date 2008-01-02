%define name 	x48
%define version 0.4.3
%define release %mkrel 4
	
%define x11_prefix      /usr/X11R6
Name:      	%name
Summary:   	X48 is an HP 48 GX emulator
Version:   	%version
Release:  	%release
License: 	GPL
Group:     	Sciences/Mathematics
URL:            https://sourceforge.net/projects/x48/
Source:    	%name-%{version}.tar.gz
#Patch:    	x48.patch
Buildrequires:	readline-devel, X11-devel, imake, x11-util-cf-files, ncurses-devel
Requires:  	readline

%description
This is an emulator of the HP 48 SX and GX calculator.
Romdumps are available from http://x48.berlios.de/

%prep
%setup -q

%build
xmkmf
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_defaultdocdir}/%{name}-%{version}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
make DESTDIR=$RPM_BUILD_ROOT PROJECTROOT=/usr BINDIR=%{_bindir} install
make DESTDIR=$RPM_BUILD_ROOT PROJECTROOT=/usr MANPATH=%{_mandir} DOCDIR=%{_defaultdocdir}/%{name}-%{version} install.man

rm -rf $RPM_BUILD_ROOT/x11_prefix
rm -rf  $RPM_BUILD_ROOT/usr/lib/X11

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/

cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=x48 -rom /usr/share/x48/rom
Name=x48
Comment=HP48 Emulator
Categories=Office;
EOF

cat > $RPM_BUILD_DIR/%{name}-%{version}/README.urpmi << EOF
x48 needs a rom to function, so please read the README to see how to dump it
from your HP48 or just use the rpm x48-gxrom or x48-sxrom from plf.
If you dump the rom, please put it in the /usr/share/x48 directory.
***
The first time you launch x48, it will copy the rom to ~/.hp48.
So if you like to change from sx to gx rom, please remove this directory first
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root,-)
%doc	README README.urpmi
%{_sysconfdir}/X11/app-defaults/X48
%{_bindir}/checkrom
%{_bindir}/dump2rom
%{_bindir}/mkcard
%{_bindir}/x48
%{_datadir}/%{name}
#   /usr/X11R6/lib/X11/doc/html/x48.1.html
%{_mandir}/man1/x48.*
%{_datadir}/applications/mandriva-x48.desktop
