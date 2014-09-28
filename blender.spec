# String format build errors are mostly avoided by gcc stupidity
# Only few are usually fixed by patches, it makes no sense.
# So disable check at all.
%define Werror_cflags %{nil}
%define _disable_ld_no_undefined 1

%bcond_without	cycles

Summary:	A fully functional 3D modeling/rendering/animation package
Name:		blender
Version:	2.72
Release:	1
Group:		Graphics
License:	GPLv2+
Url:		http://www.blender.org/
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
Source100:	blender.rpmlintrc
Patch0:		blender-2.67-localedir.patch
Patch1:		blender-2.60-error-when-missing-sse.patch
Patch2:		blender-2.58-static-lib.patch
Patch3:		blender-2.65-openjpeg_stdbool.patch
# Cycles build fails with undefined reference error as libs are build as shared
Patch5:		blender-2.72-cycles-static.patch
# Patch submitted upstream - Blender Patches item #19234,
Patch6:		blender-2.67-uninit-var.patch

BuildRequires:	cmake >= 2.8
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel >= 0.7
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
%setup -q
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

