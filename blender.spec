# String format build errors are mostly avoided by gcc stupidity
# Only few are usually fixed by patches, it makes no sense.
# So disable check at all.
%define Werror_cflags %{nil}
%define _disable_ld_no_undefined 1
# As of blender 3.0.1, clang 13.0.0, building with full LTO takes
# enough RAM to bring down all builders
%global optflags %{optflags} -Wno-error=float-conversion -flto=thin

%bcond_without cycles
%bcond_without opensubdiv

Summary:	A fully functional 3D modeling/rendering/animation package
Name:		blender
Version:	3.0.1
Release:	1
Group:		Graphics
License:	GPLv2+
Url:		http://www.blender.org/
Source0:	https://download.blender.org/source/blender-%{version}.tar.xz
Source100:	blender.rpmlintrc
Patch2:		blender-2.58-static-lib.patch
Patch3:		blender-2.65-openjpeg_stdbool.patch
#Patch4:		blender-2.79b-icu-linkage.patch
# Patch submitted upstream - Blender Patches item #19234,
#Patch6:		blender-2.67-uninit-var.patch
Patch12:	blender-2.79-scripts.patch
Patch13:	blender-2.79-thumbnailer.patch
Patch14:	blender-2.93.5-openexr3.patch
Patch15:	blender-2.93.5-fix-and-workaround-warnings.patch
Patch16:	https://raw.githubusercontent.com/UnitedRPMs/blender/master/blender-oiio-2.3.patch
Patch17:	blender-3.0.0-ffmpeg-5.0.patch

%if %{with opensubdiv}
BuildRequires:  opensubdiv-devel
%endif
BuildRequires:	ninja
BuildRequires:	clang
BuildRequires:	cmake >= 2.8
BuildRequires:	pkgconfig(audaspace)
BuildRequires:	cmake(pugixml)
BuildRequires:  cmake(OpenCOLLADA)
BuildRequires:	boost-devel
BuildRequires:	boost-static-devel
BuildRequires:	ffmpeg-devel >= 0.7
BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	cmake(Alembic)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	potrace-devel
BuildRequires:	libharu-devel
BuildRequires:	python-numpy
BuildRequires:	python-requests
BuildRequires:  python-numpy-devel
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:  pkgconfig(libunwind-llvm)
BuildRequires:  pkgconfig(gmpxx)
BuildRequires:	pkgconfig(libxml-2.0)
%if %with cycles
BuildRequires:	OpenImageIO
BuildRequires:	OpenImageIO-devel
BuildRequires:	pkgconfig(OpenColorIO)
%endif
Requires:	python >= 3.5

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
%autosetup -p1

%build
%cmake \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DWITH_SYSTEM_EIGEN3:BOOL=ON \
	-DWITH_SYSTEM_GLEW:BOOL=ON \
	-DWITH_SYSTEM_LZO:BOOL=ON \
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_GAMEENGINE:BOOL=ON \
	-DWITH_PLAYER:BOOL=ON \
	-DWITH_PYTHON:BOOL=ON \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
	-DPYTHON_VERSION:STRING=%{py3_ver} \
	-DPYTHON_REQUESTS_PATH:STRING=%{py3_puresitedir} \
	-DWITH_BUILTIN_GLEW:BOOL=OFF \
	-DWITH_CODEC_FFMPEG:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_MOD_OCEANSIM:BOOL=ON \
	-DWITH_IMAGE_REDCODE:BOOL=ON \
        -DWITH_SDL:BOOL=ON \
        -DWITH_JACK:BOOL=ON \
        -DWITH_INPUT_NDOF:BOLL=ON \
        -DWITH_OPENCOLORIO:BOOL=ON \
        -DWITH_DOC_MANPAGE:BOOL=ON \
	-DWITH_TBB:BOOL=ON \
	-DWITH_CYCLES_EMBREE:BOOL=OFF \
	-DCMAKE_CXX_STANDARD=17 \
%if %with cycles
	-DWITH_CYCLES:BOOL=ON \
%else
	-DWITH_CYCLES:BOOL=OFF \
%endif
	-DWITH_RAYOPTIMIZATION:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
# Somehow blender gets its own install paths wrong
PATHVER="$(basename %buildroot}%{_datadir}/blender/[0-9]*)"
mv %{buildroot}%{_datadir}/blender/scripts/addons/{*,.github} %{buildroot}%{_datadir}/blender/${PATHVER}/scripts/addons/
rmdir %{buildroot}%{_datadir}/blender/scripts/addons
mv %{buildroot}%{_datadir}/blender/scripts/* %{buildroot}%{_datadir}/blender/${PATHVER}/scripts/
rmdir %{buildroot}%{_datadir}/blender/scripts

# Install hicolor icons.
mkdir -p %{buildroot}%{_datadir}/icons/hicolor
cp -a release/freedesktop/icons/* %{buildroot}%{_datadir}/icons/hicolor/

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
%{_datadir}/doc/blender/license/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/doc/%{name}/*.txt
