#Module-Specific definitions
%define mod_name mod_variety
%define mod_conf 78_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module to serve random files from a directory
Name:		apache-%{mod_name}
Version:	0.2.1
Release:	16
Group:		System/Servers
License:	BSD
URL:		https://pmade.org/pjones/software/mod_variety/
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
%{_bindir}/apxs -c %{mod_name}.c

%install

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

%files
%doc README.html docs/manual/*.xml docs/CREDITS docs/manual.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-15mdv2012.0
+ Revision: 773233
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-14
+ Revision: 678432
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-13mdv2011.0
+ Revision: 588078
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-12mdv2010.1
+ Revision: 516212
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-11mdv2010.0
+ Revision: 406666
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-10mdv2009.1
+ Revision: 326269
- rebuild

  + Michael Scherer <misc@mandriva.org>
    - better summary

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-9mdv2009.0
+ Revision: 235118
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-8mdv2009.0
+ Revision: 215662
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-7mdv2008.1
+ Revision: 181951
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.2.1-6mdv2008.1
+ Revision: 170757
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-5mdv2008.0
+ Revision: 82691
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.1-4mdv2007.1
+ Revision: 140768
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-3mdv2007.1
+ Revision: 79535
- Import apache-mod_variety

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-3mdv2007.0
- rebuild

* Tue Dec 13 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-2mdk
- rebuilt against apache-2.2.0
- fix the conf

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.1-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.2.1-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.2.1-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2.1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.2.1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.2.1-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.2.1-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.2.1-1mdk
- built for apache 2.0.49

