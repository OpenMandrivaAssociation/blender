# String format build errors are mostly avoided by gcc stupidity
# Only few are usually fixed by patches, it makes no sense.
# So disable check at all.
%define Werror_cflags %{nil}
%define _disable_ld_no_undefined 1
%define _disable_lto 1

%bcond_without	cycles
%bcond_without opensubdiv

Summary:	A fully functional 3D modeling/rendering/animation package
Name:		blender
Version:	2.82
Release:	1
Group:		Graphics
License:	GPLv2+
Url:		http://www.blender.org/
Source0:	https://download.blender.org/source/%{name}-%{version}.tar.xz
Source100:	blender.rpmlintrc
Patch2:		blender-2.58-static-lib.patch
Patch3:		blender-2.65-openjpeg_stdbool.patch
Patch4:		blender-2.79b-icu-linkage.patch
# Patch submitted upstream - Blender Patches item #19234,
Patch6:		blender-2.67-uninit-var.patch
Patch12:	blender-2.79-scripts.patch
Patch13:	blender-2.79-thumbnailer.patch
%if %{with opensubdiv}
BuildRequires:  opensubdiv-devel
%endif
BuildRequires:	ninja
BuildRequires:	cmake >= 2.8
BuildRequires:	pkgconfig(audaspace)
BuildRequires:	cmake(pugixml)
BuildRequires:	boost-devel
BuildRequires:	boost-static-devel
BuildRequires:	ffmpeg-devel >= 0.7
BuildRequires:	gomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	icu-devel
BuildRequires:	jemalloc-devel
BuildRequires:	cmake(Alembic)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(openal)
BuildRequires:	cmake(TBBMake)
%if %mdvver <= 3000000
BuildRequires:	pkgconfig(python-3.6)
%else
BuildRequires:	pkgconfig(python3)
%endif
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	python-numpy
BuildRequires:	python-requests
BuildRequires:  python-numpy-devel
BuildRequires:	llvm-devel
%if %with cycles
BuildRequires:	OpenImageIO-devel
BuildRequires:	pkgconfig(OpenColorIO)
%endif
%if %mdvver <= 3000000
Requires:	python3.6
%else
Requires:	python3 >= 3.5
%endif

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
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_GAMEENGINE:BOOL=ON \
	-DWITH_PLAYER:BOOL=ON \
	-DWITH_PYTHON:BOOL=ON \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
%if %mdvver <= 3000000
        -DPYTHON_VERSION:STRING=%{py36_ver} \
        -DPYTHON_REQUESTS_PATH:STRING=%{py36_puresitedir} \
%else
	-DPYTHON_VERSION:STRING=%{py3_ver} \
	-DPYTHON_REQUESTS_PATH:STRING=%{py3_puresitedir} \
%endif
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
	-DOPENJPEG_ROOT_DIR=%{_libdir}/openjpeg-1.5 \
	-DWITH_TBB:BOOL=ON \
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
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/doc/%{name}/*.txt
