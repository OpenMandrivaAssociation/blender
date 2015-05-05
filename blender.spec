# String format build errors are mostly avoided by gcc stupidity
# Only few are usually fixed by patches, it makes no sense.
# So disable check at all.
%define Werror_cflags %{nil}
%define _disable_ld_no_undefined 1

%bcond_without	cycles

Summary:	A fully functional 3D modeling/rendering/animation package
Name:		blender
Version:	2.70a
Release:	3
Group:		Graphics
License:	GPLv2+
Url:		http://www.blender.org/
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
Patch0:		blender-2.67-localedir.patch
Patch1:		blender-2.60-error-when-missing-sse.patch
Patch2:		blender-2.58-static-lib.patch
Patch3:		blender-2.65-openjpeg_stdbool.patch
# Cycles build fails with undefined reference error as libs are build as shared
Patch5:		blender-2.70a-cycles-static.patch
# Patch submitted upstream - Blender Patches item #19234,
Patch6:		blender-2.67-uninit-var.patch

BuildRequires:	cmake >= 2.8
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel >= 2.5.4
BuildRequires:	gomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	openjpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
%if %with cycles
BuildRequires:	OpenImageIO-devel
BuildRequires:	OpenColorIO-devel
%endif
Requires:	python3 >= 3.3

%description
Blender is the in-house software of a high quality animation studio.
It has proven to be an extremely fast and versatile design instrument.
The software has a personal touch, offering a unique approach to the
world of three dimensions. Blender can be used to create TV
commercials, to make technical visualizations or business graphics, to
do some morphing, or to design user interfaces. Developers can easily
build and manage complex environments. The renderer is versatile and
extremely fast. All basic animation principles (curves and keys) are
implemented.

%prep
%setup -q -n %{name}-v%{version}
#patch0 -p1 -b .localedir
%patch1 -p0 -b .sse
%patch2 -p0 -b .static
%patch3 -p1 -b .openjpeg
%patch5 -p1 -b .cycles-static
%patch6 -p1

%build
%ifarch %{ix86}
# build non-sse flavour
%cmake \
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_PLAYER:BOOL=ON \
	-DWITH_PYTHON:BOOL=ON \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
	-DWITH_BUILTIN_GLEW:BOOL=OFF \
	-DWITH_CODEC_FFMPEG:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_MOD_OCEANSIM:BOOL=ON \
	-DWITH_IMAGE_REDCODE:BOOL=ON \
	-DOPENJPEG_ROOT_DIR=/usr/include/openjpeg-1.5 \
%if %with cycles
	-DWITH_CYCLES:BOOL=ON \
%else
	-DWITH_CYCLES:BOOL=OFF \
%endif
	-DWITH_RAYOPTIMIZATION:BOOL=OFF
%make
cd ..
mv build non-sse
%endif

#build sse flavour
%cmake \
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_PLAYER:BOOL=ON \
	-DWITH_PYTHON:BOOL=ON \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
	-DWITH_BUILTIN_GLEW:BOOL=OFF \
	-DWITH_CODEC_FFMPEG:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_MOD_OCEANSIM:BOOL=ON \
	-DWITH_IMAGE_REDCODE:BOOL=ON \
	-DOPENJPEG_ROOT_DIR=/usr/include/openjpeg-1.5 \
%if %with cycles
	-DWITH_CYCLES:BOOL=ON \
%else
	-DWITH_CYCLES:BOOL=OFF \
%endif
	-DWITH_RAYOPTIMIZATION:BOOL=ON
%make

%install
#install sse flavour
%makeinstall_std -C build

# Install hicolor icons.
for i in 16x16 22x22 32x32 48x48 256x256 ; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}/apps
  install -pm 0644 release/freedesktop/icons/${i}/apps/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm 0644 release/freedesktop/icons/scalable/apps/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%ifarch %{ix86}
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.sse

#install non-sse flavour
rm -fr build
mv non-sse build
%makeinstall_std -C build
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.nonsse

# install wrapper
cat >> %{buildroot}%{_bindir}/blender <<EOF 
if [ -e /proc/cpuinfo ]; then
	SSE="\`cat /proc/cpuinfo | grep flags | grep sse\`"
fi

if [ "x\$SSE" == x ]; then
	%{_bindir}/%{name}.nonsse "\$@"
else
	%{_bindir}/%{name}.sse "\$@"
fi
EOF
chmod 0755 %{buildroot}%{_bindir}/blender
%endif

sed -i -e 's,#!/usr/bin/python,#!/usr/bin/python3,' %{buildroot}%{_bindir}/blender-thumbnailer.py %{buildroot}%{_datadir}/%{name}/*/scripts/modules/blend_render_info.py

%post
if [ -x %{_gconftool_bin} ]; then
   %{_gconftool_bin} --direct --config-source xml:readwrite:%{_sysconfdir}/gconf/gconf.xml.defaults --type boolean --set /desktop/gnome/thumbnailers/application@x-blender/enable true
   %{_gconftool_bin} --direct --config-source xml:readwrite:%{_sysconfdir}/gconf/gconf.xml.defaults --type string --set /desktop/gnome/thumbnailers/application@x-blender/command "blender-thumbnailer.py %u %o"
fi

%preun
if [ "$1" = "0" -a -x %{_gconftool_bin} ]; then
   %{_gconftool_bin} --direct --config-source xml:readwrite:%{_sysconfdir}/gconf/gconf.xml.defaults --unset /desktop/gnome/thumbnailers/application@x-blender/enable
   %{_gconftool_bin} --direct --config-source xml:readwrite:%{_sysconfdir}/gconf/gconf.xml.defaults --unset /desktop/gnome/thumbnailers/application@x-blender/command
fi

%files
%doc release/text/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_iconsdir}/hicolor/*/apps/%{name}.*


%changelog
* Sun Apr 20 2014 Crispin Boylan <crisb@mandriva.org> 2.70a-1
+ Revision: 95b505a
- Fix cycles patch

* Sun Apr 20 2014 Crispin Boylan <crisb@mandriva.org> 2.70a-1
+ Revision: 68648b0
- Fix files

* Sat Apr 19 2014 Crispin Boylan <crisb@mandriva.org> 2.70a-1
+ Revision: 56ab625
- Fix build

* Sat Apr 19 2014 Crispin Boylan <crisb@mandriva.org> 2.70a-1
+ Revision: 3eeaf21
- Merge

* Sat Apr 19 2014 Crispin Boylan <crisb@mandriva.org> 2.70a-1
+ Revision: c5732cb
- 2.70a

* Sat Feb 08 2014 Tomasz Paweł Gajc <tpgxyz@gmail.com> 2.68a-2
+ Revision: 9ec362c
- MassBuild#328: Increase release tag

* Fri Dec 06 2013 Bernhard Rosenkraenzer <bero@bero.eu> 2.69-5
+ Revision: ff60c5f
- MassBuild#289: Increase release tag

* Fri Dec 06 2013 Bernhard Rosenkraenzer <bero@bero.eu> 2.69-4
+ Revision: 5305424
- MassBuild#289: Increase release tag

* Fri Dec 06 2013 Bernhard Rosenkraenzer <bero@bero.eu> 2.69-3
+ Revision: 4746181
- MassBuild#289: Increase release tag

* Fri Dec 06 2013 Bernhard Rosenkraenzer <bero@bero.eu> 2.69-2
+ Revision: 2666a45
- MassBuild#289: Increase release tag

* Sun Nov 24 2013 Crispin Boylan <crisb@mandriva.org> 2.69-1
+ Revision: 1de6f20
- 2.69

* Thu Aug 22 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 2.68a-1
+ Revision: a476130
- LOG New version 2.68a

* Thu Jun 06 2013 Bernhard Rosenkraenzer <Bernhard.Rosenkranzer@linaro.org> 2.67b-1
+ Revision: 3d44569
- BR pkgconfig(glu)

* Thu Jun 06 2013 Bernhard Rosenkraenzer <Bernhard.Rosenkranzer@linaro.org> 2.67b-1
+ Revision: 00287ad
- 2.67b

* Mon May 13 2013 Denis Silakov <denis.silakov@rosalab.ru> 2.67-1
+ Revision: 663b6ed
- LOG Updated to 2.67

* Fri Mar 15 2013 Andrey Bondrov <andrey.bondrov@rosalab.ru> 2.66a-1
+ Revision: 5fc94b0
- LOG New version 2.66a, re-diff some patches, disable string format security check as it's useless here

* Sun Mar 10 2013 mdawkins (Matthew Dawkins) <mattydaw@gmail.com> 2.65a-1
+ Revision: cca9e1a
- cleaned up spec

* Wed Feb 20 2013 Crispin Boylan <crisb@mandriva.org> 2.65a-1
+ Revision: d3daa77
- Fix patch apply

* Wed Feb 20 2013 Crispin Boylan <crisb@mandriva.org> 2.65a-1
+ Revision: ae9bbc4
- Update patches (from mageia)

* Wed Feb 20 2013 Crispin Boylan <crisb@mandriva.org> 2.65a-1
+ Revision: a13b8d1
- 2.65a with python 3.3 support

* Wed Feb 20 2013 Crispin Boylan <crisb@mandriva.org> 2.64-4
+ Revision: a0cf363
- Fix BR

* Sat Dec 08 2012 alex <alex@localhost.localdomain> 2.64-3
+ Revision: e354eb6
- merging with rosa2012.1 of project blender

* Sun Oct 07 2012 abondrov <abondrov@mandriva.org> 2.64-3
+ Revision: 8c06e89
- Use better patch for locales dir
- SILENT: svn-revision: 818647

* Sat Oct 06 2012 abondrov <abondrov@mandriva.org> 2.64-2
+ Revision: 3325360
- New version 2.64, convert BR to pkgconfig style, update patchset, build with Cycles engine enabled
- SILENT: svn-revision: 818596

* Sun May 13 2012 bero <bero@mandriva.org> 2.63a-1
+ Revision: 3f80d49
- Update to 2.63a
- SILENT: svn-revision: 798688

* Fri Apr 27 2012 bero <bero@mandriva.org> 2.63-1
+ Revision: ab58a47
- Update to 2.63
- SILENT: svn-revision: 794163

* Sat Feb 18 2012 abondrov <abondrov@mandriva.org> 2.62-2
+ Revision: a994844
- Bump release
- SILENT: svn-revision: 776757

* Sat Feb 18 2012 abondrov <abondrov@mandriva.org> 2.62-1
+ Revision: 3c077a5
- Add boost-devel to BuildRequires
- SILENT: svn-revision: 776557

* Sat Feb 18 2012 abondrov <abondrov@mandriva.org> 2.62-1
+ Revision: 8055a71
- New version 2.62
- SILENT: svn-revision: 776479

* Thu Dec 15 2011 abondrov <abondrov@mandriva.org> 2.61-1
+ Revision: 70553d8
- New version 2.61, do not build Cycles rendering engine yet
- SILENT: svn-revision: 741400

* Fri Oct 28 2011 abondrov <abondrov@mandriva.org> 2.60a-1
+ Revision: 7961155
- New bugfix version 2.60a
- SILENT: svn-revision: 707682

* Mon Oct 24 2011 abondrov <abondrov@mandriva.org> 2.60-1
+ Revision: 7142c4e
- New version 2.60, no support for python < 3.2 yet (disable patches)
- SILENT: svn-revision: 705918

* Sun Aug 14 2011 fwang <fwang@mandriva.org> 2.59-1
+ Revision: 335bb78
- new version 2.59
- SILENT: svn-revision: 694445

* Mon Aug 08 2011 kazancas <kazancas@mandriva.org> 2.58a-2
+ Revision: aad6e25
- SILENT fix requires libpython3.2
- SILENT: svn-revision: 693687

* Mon Aug 08 2011 kazancas <kazancas@mandriva.org> 2.58a-2
+ Revision: 1a709a9
- SILENT fix build requires
- SILENT: svn-revision: 693675


