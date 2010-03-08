#Module-Specific definitions
%define mod_name mod_variety
%define mod_conf 78_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module to serve random files from a directory
Name:		apache-%{mod_name}
Version:	0.2.1
Release:	%mkrel 12
Group:		System/Servers
License:	BSD
URL:		http://pmade.org/pjones/software/mod_variety/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Source2:	README.html.variety.bz2
Patch0:		%{mod_name}-0.2.0-register.patch
Patch1:		mod_variety-0.2.1-apache220.diff
BuildRequires:	unzip
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_variety is an Apache 2.x module that will serve a random file
from the requested directory. It is useful for serving random
images or completely random sites. 

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0
bzcat %{SOURCE2} > README.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

# fix strange file permissions
find -type f|xargs chmod 644

cp src/%{mod_name}.c %{mod_name}.c

# make doesn't work, but this does (real qute!)
%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.html docs/manual/*.xml docs/CREDITS docs/manual.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


