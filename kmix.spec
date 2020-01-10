Name:    kmix 
Summary: KDE volume control 
Version: 4.10.5
Release: 4%{?dist}

# code is LGPLv2+ except for gui/osdwidget.* which is GPLv2+
# docs GFDL
License: GPLv2+ and GFDL
URL:     https://projects.kde.org/projects/kde/kdemultimedia/%{name}
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstream patches
# pull a few from master/ branch, not officially backported
Patch101: 0001-MPRIS2-backend-now-does-a-asynchonous-DBUS-instrospe.patch
Patch102: 0002-Use-a-fixed-volume-step-of-n-instead-of-honoring-mou.patch
Patch103: 0003-Global-Keyboard-Shortcuts-XF86Audio-now-only-affect-.patch
Patch104: 0004-memoryLeak.patch
Patch105: 0005-Less-debugging-output.patch
Patch106: 0006-Revert-my-direct-use-of-ControlManager-instance-.ann.patch

BuildRequires: desktop-file-utils
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(phonon)

Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}

# when split occurred
Obsoletes: kdemultimedia-kmix < 6:4.8.80
Provides:  kdemultimedia-kmix = 6:%{version}-%{release}


%description
%{summary}.


%prep
%setup -q

%patch101 -p1 -b .0001
%patch102 -p1 -b .0002
%patch103 -p1 -b .0003
%patch104 -p1 -b .0004
%patch105 -p1 -b .0005
%patch106 -p1 -b .0006


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# fix documentation multilib conflict in index.cache
bunzip2 %{buildroot}%{_kde4_docdir}/HTML/en/kmix/index.cache.bz2
sed -i -e 's!name="id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/kmix/index.cache
sed -i -e 's!#id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/kmix/index.cache
bzip2 -9 %{buildroot}%{_kde4_docdir}/HTML/en/kmix/index.cache

%find_lang %{name} --with-kde --without-mo


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/kmix.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING COPYING.DOC TODO
%{_kde4_appsdir}/kmix/
%{_kde4_appsdir}/plasma/services/mixer.operations
%{_kde4_bindir}/kmix
%{_kde4_bindir}/kmixctrl
%{_kde4_datadir}/applications/kde4/kmix.desktop
%{_kde4_datadir}/autostart/*.desktop
%{_kde4_datadir}/dbus-1/interfaces/org.kde.kmix.control.xml
%{_kde4_datadir}/dbus-1/interfaces/org.kde.kmix.mixer.xml
%{_kde4_datadir}/dbus-1/interfaces/org.kde.kmix.mixset.xml
%{_kde4_datadir}/kde4/services/kded/kmixd.desktop
%{_kde4_datadir}/kde4/services/kmixctrl_restore.desktop
%{_kde4_datadir}/kde4/services/plasma-engine-mixer.desktop
%{_kde4_iconsdir}/hicolor/*/*/kmix.*
%{_kde4_libdir}/libkdeinit4_kmix.so
%{_kde4_libdir}/libkdeinit4_kmixctrl.so
%{_kde4_libdir}/kde4/kded_kmixd.so
%{_kde4_libdir}/kde4/plasma_engine_mixer.so


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.10.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.10.5-3
- Mass rebuild 2013-12-27

* Thu Jul 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.5-2
- backport memleak-on-track-change fix (kde#309464, #912457)

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Thu Apr 25 2013 Than Ngo <than@redhat.com> - 4.10.2-3
- fix multilib issue

* Wed Apr 17 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-2
- backport some patches from master branch

* Mon Apr 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Mon Mar 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-2
- pull a few upstream patches, in particular...
- kmix crahes moving streams between sinks (#922849)

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Thu Nov 22 2012 Than Ngo <than@redhat.com> - 4.9.3-2
- fix license issue

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.95-1
- 4.8.95

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-2
- License: GPLv2+ and GFDL

* Fri Jun 08 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-1
- kmix-4.8.90

