%define name 	x48
%define version 0.6.3
%define release %mkrel 2

#define x11_prefix      /usr/X11R6

Name:		%name
Summary:	HP 48 GX emulator
Version:	%version
Release:	%release
License:	GPL
Group:		Sciences/Mathematics
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://x48.berlios.de/
Source0:	http://download.berlios.de/x48/%{name}-%{version}.tar.gz
Patch0:		x48-0.6.1-mdv-fix-string-format.patch
BuildRequires:	readline-devel
BuildRequires:	X11-devel
BuildRequires:	x11-util-cf-files
BuildRequires:	ncurses-devel
Requires:  	readline

%description
This is an emulator of the HP 48 SX and GX calculator.
Romdumps are available from http://x48.berlios.de/

%prep
%setup -q
%patch0 -p1 -b .format

%build
%configure2_5x --with-x
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/applications/

cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=x48 -rom /usr/share/x48/rom
Name=x48
Comment=HP48 Emulator
Categories=Office;
EOF

cat > %{_builddir}/%{name}-%{version}/README.urpmi << EOF
x48 needs a rom to function, so please read the README to see how to dump it
from your HP48 or just use the rpm x48-gxrom or x48-sxrom from plf.
If you dump the rom, please put it in the /usr/share/x48 directory.
***
The first time you launch x48, it will copy the rom to ~/.hp48.
So if you like to change from sx to gx rom, please remove this directory first
EOF

%makeinstall_std

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc	README README.urpmi
#%{_sysconfdir}/X11/app-defaults/X48
%{_bindir}/checkrom
%{_bindir}/dump2rom
%{_bindir}/mkcard
%{_bindir}/x48
%{_datadir}/%{name}
%{_datadir}/X11/app-defaults/X48
%{_mandir}/man1/x48.*
%{_datadir}/applications/mandriva-x48.desktop
