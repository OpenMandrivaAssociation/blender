# String format build errors are mostly avoided by gcc stupidity
# Only few are usually fixed by patches, it makes no sense.
# So disable check at all.
%define Werror_cflags %{nil}
%define _disable_ld_no_undefined 1
# OpenVDB volume.cc (and the blender+USD link) OOMs builders under LTO.
%define _disable_lto 1
%ifarch %{armx}
# -isystem %%{_sourcedir} is for sse2neon.h
# WITH_COMPILER_SIMD is off below: blender's default
# -march=armv8.2-a+dotprod+fp16+lse SIGILLs makesdna on v8.0 builders.
%global optflags %{optflags} -Wno-error=float-conversion -isystem %{_sourcedir}
%else
%global optflags %{optflags} -Wno-error=float-conversion
%endif
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

%bcond cycles 1
%bcond opensubdiv 1

Summary:	A fully functional 3D modeling/rendering/animation package
Name:		blender
Version:	5.2.1
Release:	2
Group:		Graphics
License:	GPL-2.0-or-later
URL:		https://www.blender.org/
Source0:	https://download.blender.org/source/blender-%{version}.tar.xz
Source1:	https://raw.githubusercontent.com/DLTcollab/sse2neon/master/sse2neon.h
Source100:	blender.rpmlintrc
#Patch1:		blender-3.6.2-link-libatomic.patch 
Patch2:		blender-2.58-static-lib.patch
#Patch3:		blender-2.65-openjpeg_stdbool.patch
#Patch4:		blender-2.79b-icu-linkage.patch
# Patch submitted upstream - Blender Patches item #19234,
#Patch6:		blender-2.67-uninit-var.patch
Patch12:	blender-2.79-scripts.patch
Patch13:	blender-2.79-thumbnailer.patch
#Patch14:	blender-4.3.0-znver1-avx512.patch
#Patch15:	blender-2.93.5-fix-and-workaround-warnings.patch
#Patch16:	https://raw.githubusercontent.com/UnitedRPMs/blender/master/blender-oiio-2.3.patch
#Patch17:	blender-3.0.0-ffmpeg-5.0.patch
# fmtlib is no longer bundled; 5.2 uses system fmt
#Patch18:	blender-4.5.0-compile.patch
#Patch24:	https://src.fedoraproject.org/rpms/blender/raw/rawhide/f/0001-Support-Python-3.11b3.patch
#Patch25:	https://src.fedoraproject.org/rpms/blender/raw/rawhide/f/blender-usd-pythonlibs-fix.diff
#Patch26:	https://src.fedoraproject.org/rpms/blender/raw/rawhide/f/blender-python310.patch
#Patch27:	blender-4.5.0-ffmpeg-8.0.patch
# Upstream in 5.1+
# See	https://projects.blender.org/blender/blender/commit/7b19e74cadadc5db30aafe2f5539170501469c0d
#Patch19:	fix-SIMD-detection-intrinsics-auto-vectorization-eigen-headers.patch

%if %{with opensubdiv}
BuildRequires:	opensubdiv-devel
%endif
BuildRequires:	ninja
BuildRequires:	clang
BuildRequires:	cmake >= 2.8
BuildRequires:	pkgconfig(audaspace)
BuildRequires:	cmake(pugixml)
BuildRequires:	cmake(OpenCOLLADA)
BuildRequires:	boost-devel
BuildRequires:	boost-static-devel
BuildRequires:	ffmpeg-devel >= 0.7
BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	cmake(Alembic)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libdecor-0)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(openxr)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sdl3)
BuildRequires:	cmake(fmt)
BuildRequires:	pkgconfig(shaderc)
BuildRequires:	pkgconfig(spnav)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	potrace-devel
BuildRequires:	libharu-devel
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python-numpy-devel
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:	llvm-static-devel
BuildRequires:	cmake(Alembic)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	pkgconfig(gmpxx)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	atomic-devel
BuildRequires:	OpenImageIO
BuildRequires:	OpenImageIO-devel
BuildRequires:	pkgconfig(OpenColorIO)
BuildRequires:	cmake(Ceres)
BuildRequires:	cmake(pxr)
BuildRequires:	cmake(openpgl)
BuildRequires:	cmake(manifold)
BuildRequires:	cmake(meshoptimizer)
BuildRequires:	cmake(OSL)
# oslc compiles Cycles .osl → .oso; stdosl.h is in the common-headers subpackage.
BuildRequires:	openshadinglanguage
BuildRequires:	openshadinglanguage-common-headers
BuildRequires:	cmake(OpenVDB)
BuildRequires:	openvdb-nanovdb-devel
BuildRequires:	pkgconfig(blosc)
BuildRequires:	cmake(MaterialX)
# MaterialXConfig.cmake set_and_check()s these paths at find_package time.
BuildRequires:	materialx-data
BuildRequires:	python-materialx
BuildRequires:	materialx
BuildRequires:	cmake(OpenImageDenoise)
BuildRequires:	cmake(draco)
BuildRequires:	cmake(embree)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(harfbuzz)
Requires:	python >= 3.5
# MaterialX stdlib / OSL headers are opened by path, not ELF-linked.
Requires:	materialx-data
Requires:	openshadinglanguage-common-headers

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
# Linking blender + cycles is RAM-heavy; OOM-killer hit parallel links
# ("unable to execute command: Killed" / linker exit -2).
# FIXME we currently turn off WITH_GL_EGL
# because it results in link time errors (undefined
# references in libGLEW). This should be fixed properly
# at some point. In the mean time, GLX is good enough.
# 5.2 unbundled Ceres; system ceres-solver backs libmv/motion tracking.
# USD/Hydra, OpenPGL, Manifold, meshoptimizer, OSL, OpenVDB/NanoVDB,
# MaterialX, OpenImageDenoise, Draco and Embree are system packages.
%cmake \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DWITH_SYSTEM_EIGEN3:BOOL=ON \
	-DWITH_SYSTEM_GLEW:BOOL=ON \
	-DWITH_SYSTEM_LZO:BOOL=ON \
	-DWITH_SYSTEM_AUDASPACE:BOOL=ON \
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
	-DWITH_RUBBERBAND:BOOL=ON \
	-DWITH_XR_OPENXR:BOOL=ON \
	-DWITH_SDL_AUDIO:BOOL=ON \
	-DWITH_JACK:BOOL=ON \
	-DWITH_INPUT_NDOF:BOOL=ON \
	-DWITH_DOC_MANPAGE:BOOL=ON \
	-DWITH_TBB:BOOL=ON \
	-DWITH_CYCLES_EMBREE:BOOL=ON \
	-DWITH_CYCLES_OSL:BOOL=ON \
	-DWITH_OPENVDB:BOOL=ON \
	-DWITH_OPENVDB_BLOSC:BOOL=ON \
	-DWITH_NANOVDB:BOOL=ON \
	-DWITH_MATERIALX:BOOL=ON \
	-DWITH_OPENIMAGEDENOISE:BOOL=ON \
	-DWITH_DRACO:BOOL=ON \
	-DWITH_FRIBIDI:BOOL=ON \
	-DWITH_HARFBUZZ:BOOL=ON \
	-DWITH_LIBS_PRECOMPILED:BOOL=OFF \
	-DWITH_LIBMV:BOOL=ON \
	-DWITH_USD:BOOL=ON \
	-DWITH_HYDRA:BOOL=ON \
	-DWITH_CYCLES_PATH_GUIDING:BOOL=ON \
	-DWITH_MANIFOLD:BOOL=ON \
	-DWITH_MESHOPTIMIZER:BOOL=ON \
	-DCMAKE_CXX_STANDARD=20 \
%ifarch %{armx}
	-DSSE2NEON_INCLUDE_DIR=%{_sourcedir} \
	-DWITH_COMPILER_SIMD:BOOL=OFF \
%endif
%if %with cycles
	-DWITH_CYCLES:BOOL=ON \
%else
	-DWITH_CYCLES:BOOL=OFF \
%endif
	-DWITH_RAYOPTIMIZATION:BOOL=ON \
	-G Ninja
# Cap parallelism: OpenVDB volume.cc plus a few neighbours OOMs at -j4.
export NINJAFLAGS="${NINJAFLAGS:--j2}"
export CMAKE_BUILD_PARALLEL_LEVEL="${CMAKE_BUILD_PARALLEL_LEVEL:-2}"
%ninja_build
touch source/creator/blender.1

%install
%ninja_install -C build
# Somehow blender gets its own install paths wrong
PATHVER="$(basename %buildroot}%{_datadir}/blender/[0-9]*)"
cp -ra %{buildroot}%{_datadir}/blender/scripts/addons_core/* %{buildroot}%{_datadir}/blender/${PATHVER}/scripts/addons_core/
rm -rf %{buildroot}%{_datadir}/blender/scripts/addons_core
cp -ra %{buildroot}%{_datadir}/blender/scripts/* %{buildroot}%{_datadir}/blender/${PATHVER}/scripts/
rm -rf %{buildroot}%{_datadir}/blender/scripts

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
%{_bindir}/blender{,-thumbnailer}
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/metainfo/org.blender.Blender.metainfo.xml
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/doc/%{name}
