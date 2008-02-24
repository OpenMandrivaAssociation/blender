%define testver		244
%define	relver		245
%define name		blender
%define truename	blender

%define build_debug     0
%{?_with_debug: %{expand: %%global build_debug 1}}
%{?_without_debug: %{expand: %%global build_debug 0}}

%define build_fullopt 1
%{?_with_fullopt: %{expand: %%global build_fullopt 1}}
%{?_without_fullopt: %{expand: %%global build_fullopt 0}}

%define use_smp		1
%{?_with_smp: %global use_smp 1}
%{?_without_smp: %global use_smp 0}

%if %{use_smp}
%define scons_smp --debug=time -j %(expr $(getconf _NPROCESSORS_ONLN) + 2)
%else
%define scons_smp %nil
%endif

Name:		%{name}
Version:	2.45
Release:	%mkrel 6
Summary:	A fully functional 3D modeling/rendering/animation package
Group:		Graphics
Source0:	http://download.blender.org/source/blender-%{version}.tar.bz2
Source1: 	blender-wrapper
Source2:	http://download.blender.org/demo/test/test%{testver}.zip
Source11:	blender-16x16.png
Source12:	blender-32x32.png
Source13:	blender-48x48.png
Source14:	blendernodri-16x16.png
Source15:	blendernodri-32x32.png
Source16:	blendernodri-48x48.png
Patch0:		blender-2.41-openal-fix.patch
Patch2:		blender-2.43-lib64.patch
Patch3:		blender-2.42-forceyafrayplug.patch
Patch5:		blender-2.41-libtiff.patch
Patch7:		blender-2.43-varuninitial.patch
Patch8:		blender-2.41-yafray-64.patch
Patch9:		blender-2.42-yafray-ncpus.patch
Patch10:	blender-2.42-O3opt.patch
Patch13:	blender-2.44-python25.patch
Patch14:	blender-2.44-alut.patch
Patch16:	blender-2.43-rc3-avclose.patch
Patch17:	blender-2.44-changelog.patch
Patch18:	blender-2.43-yafray_zero_threads.patch
Patch19:	blender-2.43-maxthreads.patch
Patch20:	blender-2.44-force-python24.patch
Patch21:	blender-2.44-boxpack2d-missed.patch
Patch22:	blender-2.44-bug6811.patch
Patch23:	blender-2.44-more-than-six-subsurf.patch
Patch24:	blender-2.45-import-dxf-logpath.patch
Patch25:	blender-2.45-r12026.patch
Patch26:	blender-2.45-r12027.patch
Patch27:	blender-2.45-r12031.patch
Patch28:	blender-2.45-r12033.patch
Patch29:	blender-2.45-r12051.patch
Patch30:	blender-2.45-r12055.patch
Patch31:	blender-2.45-r12056.patch
Patch32:	blender-2.45-r12077.patch
Patch33:	blender-2.45-r12127.patch
Patch34:	blender-2.45-deinterlace.patch
URL:		http://www.blender.org/
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	scons
BuildRequires:	openal-devel >= 0.0.6-9mdk
BuildRequires:	OpenEXR-devel
BuildRequires:	esound-devel
%if %{mdkversion} >= 200700 || "%{mdvver}" == "mlcd4"
BuildRequires:  freealut-devel
%endif
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
BuildRequires:	ffmpeg-devel >= 0.4.9-1.pre1
%endif
%if %{mdkversion} >= 200710 || "%{mdvver}" == "mlcd4"
BuildRequires:	ffmpeg-devel >= 0.4.9-3.pre1.7407.10
%endif
BuildRequires:	ftgl-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
BuildRequires:	mesaglu-devel
%else
BuildRequires:	MesaGLU-devel
%endif
BuildRequires:	oggvorbis-devel
#BuildRequires:	ode-devel
BuildRequires:	openssl-devel
BuildRequires:	png-devel
BuildRequires:	python-devel >= 2.4
BuildRequires:	SDL-devel
BuildRequires:	smpeg-devel
BuildRequires:	%{mklibname tiff 3}-devel
BuildRequires:	X11-devel
BuildRequires:	zlib-devel
Requires:	python-imaging >= 1.1.4
Requires:	yafray
Requires:	libtiff

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

%if %build_debug
This version is build with debug enabled.
%endif

%prep
%setup -q -n %{truename}-%{version} -a 2
%patch0 -p1 -b .openal
%if "%{_lib}" != "lib"
%patch2 -p1 -b .lib64
%endif
%patch3 -p1 -b .yafray
%patch5 -p1 -b .libtiff
%patch7 -p1 -b .varun
%patch8 -p1 -b .yafray64
%patch9 -p1 -b .ncpus
%patch10 -p1 -b .O3opt
%if %{mdkversion} >= 200710 || "%{mdvver}" == "mlcd4"
%patch13 -p1 -b .python
%else
%patch20 -p1 -b .python24
%endif
%if %{mdkversion} >= 200700 || "%{mdvver}" =="mlcd4"
%patch14 -p1 -b .alut
%endif
%patch16 -p1 -b .imgbro
%patch17 -p1 -b .chglog
%patch18 -p1 -b .zero_threads
%patch19 -p1 -b .maxthreads
%patch21 -p1
%patch22 -p1 -b .bug6811
%patch23 -p1 -b .subsurf
%patch24 -p1 -b .dxflogpath
%patch25 -p1 -b .12026
%patch26 -p1 -b .12027
%patch27 -p1 -b .12031
%patch28 -p1 -b .12033
%patch29 -p1 -b .12051
%patch30 -p1 -b .12055
%patch31 -p1 -b .12056
%patch32 -p1 -b .12077
%patch33 -p1 -b .12127
%patch34 -p1 -b .deinterlace

# Fix pt_BR
sed -i "s,pt_br,pt_BR,g" bin/.blender/.Blanguages
mv bin/.blender/locale/pt_br bin/.blender/locale/pt_BR

%build
%if %{build_debug}
%define debug_flags -g
%define scons_debug BF_DEBUG=1
%else
%define debug_flags ""
%define scons_debug BF_DEBUG=0
%endif

cat > user-config.py <<EOF
BF_GETTEXT_LIBPATH = '\${BF_GETTEXT}/%{_lib}'
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
WITH_BF_FFMPEG = 'true'
%else
WITH_BF_FFMPEG = 'false'
%endif
WITH_BF_VERSE = 'true'
WITH_BF_GAMEENGINE = 'true'
WITH_BF_PLAYER = 'true'
#WITH_BF_ODE = 'true'
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
BF_OPENGL_LIBPATH = '%{_prefix}/X11R6/%{_lib}'
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 %debug_flags -ffast-math -funsigned-char -fno-strict-aliasing".split()
CXXFLAGS = "%{optflags} -O3 %debug_flags -ffast-math -funsigned-char -fno-strict-aliasing".split()
REL_CFLAGS  = "-O3".split()
REL_CCFLAGS = "-O3".split()
%endif
EOF

cat > user-config.py.sse <<EOF
BF_GETTEXT_LIBPATH = '\${BF_GETTEXT}/%{_lib}'
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
WITH_BF_FFMPEG = 'true'
%else
WITH_BF_FFMPEG = 'false'
%endif
WITH_BF_VERSE = 'true'
WITH_BF_GAMEENGINE = 'true'
WITH_BF_PLAYER = 'true'
#WITH_BF_ODE = 'true'
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
BF_OPENGL_LIBPATH = '%{_prefix}/X11R6/%{_lib}'
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 %debug_flags -ffast-math -msse -mfpmath=sse -funsigned-char -fno-strict-aliasing".split()
CXXFLAGS = "%{optflags} -O3 %debug_flags -ffast-math -msse -mfpmath=sse -funsigned-char -fno-strict-aliasing".split()
REL_CFLAGS  = "-O3".split()
REL_CCFLAGS = "-O3".split()
%endif
EOF

%ifarch %{ix86}
cp -p user-config.py user-config.py.std
cp -p user-config.py.sse user-config.py
scons -c %scons_debug BF_QUIET=0
scons %scons_debug %scons_smp BF_QUIET=0
cp -p builddir/bin/blender blender.sse
cp -p user-config.py.std user-config.py
scons -c %scons_debug BF_QUIET=0
%endif

scons %scons_debug %scons_smp BF_QUIET=0

# Build plugins
pushd release/plugins
   if [ -d ./include ]; then
	rm -rf include
   fi
   ln -s ../../source/blender/blenpluginapi include
   chmod +x bmake
   %make
popd

find ./test%{testver} -type f -print0|xargs -0 chmod 644
find ./test%{testver} -type d -print0|xargs -0 chmod 755 

%install
rm -rf %{buildroot}

install -m 755 %{SOURCE1} blender-wrapper
perl -pi -e 's@\$\{BLENDER_LIBDIR\}/%{truename}/@\$\{BLENDER_LIBDIR\}/%{name}/@g' blender-wrapper

%ifarch %{ix86}
cat >> blender-wrapper <<EOF 
if [ -e /proc/cpuinfo ]; then
	SSE="\`cat /proc/cpuinfo | grep flags | grep sse\`"
fi

if [ "x\$SSE" == x ]; then
	\${BLENDER_LIBDIR}/%{name}/%{truename} "\$@"
else
	\${BLENDER_LIBDIR}/%{name}/%{truename}.sse "\$@"
fi
EOF
%else
cat >> blender-wrapper <<EOF
\${BLENDER_LIBDIR}/%{name}/%{truename} "\$@"
EOF
%endif

install -d -m 755 \
		%{buildroot}%{_bindir} \
		%{buildroot}%{_libdir}/%{name} \
		%{buildroot}%{_datadir}

install -m 755 ./installdir/blenderplayer %{buildroot}%{_libdir}/%{name}/%{truename}player
install -m 755 ./installdir/verse %{buildroot}%{_libdir}/%{name}/verse
ln -s %{_libdir}/%{name}/%{truename}player %{buildroot}%{_bindir}/%{name}player
install -m 755 ./installdir/blender %{buildroot}%{_libdir}/%{name}/%{truename}
%ifarch %{ix86}
install -m 755 ./blender.sse %{buildroot}%{_libdir}/%{name}/%{truename}.sse
%endif
install -m 755 blender-wrapper %{buildroot}%{_bindir}/%{name}
sed -i "s,SPECDEFINED,%_libdir,g" %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}
cp -p %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}nodri
perl -pi -e 's@^\s*\$\{BLENDER_LIBDIR\}/%{name}/blender@LIBGL_ALWAYS_INDIRECT=1 \$\{BLENDER_LIBDIR\}/%{name}/blender@g' %{buildroot}%{_bindir}/%{name}nodri
cp -a ./installdir/.blender/scripts %{buildroot}%{_libdir}/%{name}
cp -a ./installdir/.blender/locale  %{buildroot}%{_datadir}
install -p -m 644 ./installdir/.blender/.Blanguages %{buildroot}%{_libdir}/%{name}
install -p -m 644 ./installdir/.blender/.bfont.ttf %{buildroot}%{_libdir}/%{name}
install -p -m 644 release/VERSION %{buildroot}%{_libdir}/%{name}
install -p -m 644 ./installdir/release_%{relver}.txt %{buildroot}%{_libdir}/%{name}
install -p -m 644 ./installdir/copyright.txt %{buildroot}%{_libdir}/%{name}
install -p -m 644 ./installdir/BlenderQuickStart.pdf %{buildroot}%{_libdir}/%{name}
install -p -m 644 ./installdir/blender.html %{buildroot}%{_libdir}/%{name}
install -p -m 644 source/blender/python/api2_2x/doc/*.py %{buildroot}%{_libdir}/%{name}/scripts
install -d -m 755 %{buildroot}%{_libdir}/%{name}/plugins/sequence
install -pD -m 644 release/plugins/sequence/*.so %{buildroot}%{_libdir}/%{name}/plugins/sequence
install -d %{buildroot}%{_libdir}/%{name}/plugins/texture
install -pD -m 644 release/plugins/texture/*.so %{buildroot}%{_libdir}/%{name}/plugins/texture
find %{buildroot}%{_libdir}/%{name}/scripts -type f -name '*.py' -exec chmod 644 '{}' \;

# menu
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Blender
Comment=The free open source 3D content creation suite
Exec=%{_bindir}/%{name} -w %f
Icon=%{name}
Terminal=false
Type=Application
Categories=3DGraphics;Graphics;Viewer;
MimeType=application/x-blender;
InitialPreference=11
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}fs.desktop << EOF
[Desktop Entry]
Name=Blender (FullScreen)
Comment=The free open source 3D content creation suite
Exec=%{_bindir}/%{name} -W %f
Icon=%{name}
Terminal=false
Type=Application
Categories=3DGraphics;Graphics;Viewer;
MimeType=application/x-blender;
InitialPreference=10
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}nodri.desktop << EOF
[Desktop Entry]
Name=Blender (DRI disabled)
Comment=The free open source 3D content creation suite (with DRI disabled)
Exec=%{_bindir}/%{name}nodri -w %f
Icon=%{name}nodri
Terminal=false
Type=Application
Categories=3DGraphics;Graphics;Viewer;
EOF
%endif

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 %{SOURCE14} -D %{buildroot}%{_miconsdir}/%{name}nodri.png
install -m644 %{SOURCE15} -D %{buildroot}%{_iconsdir}/%{name}nodri.png
install -m644 %{SOURCE16} -D %{buildroot}%{_liconsdir}/%{name}nodri.png

%if %build_debug
export DONT_STRIP=1
%endif

%clean
rm -rf %{buildroot}

%post
%{update_menus}
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
%{update_desktop_database} 
%endif

%postun
%{clean_menus}
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
%{clean_desktop_database} 
%endif

%files
%defattr(-,root,root)
%doc ChangeLog README doc/*.txt test%{testver}
%{_bindir}/*
%if %{mdkversion} >= 200610 || "%{mdvver}" == "mlcd4"
%{_datadir}/applications/*
%endif
%{_datadir}/locale/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/scripts
%{_libdir}/%{name}/%{truename}
%ifarch %{ix86}
%{_libdir}/%{name}/%{truename}.sse
%endif
%{_libdir}/%{name}/verse
%{_libdir}/%{name}/%{truename}player
%{_libdir}/%{name}/.bfont.ttf
%{_libdir}/%{name}/.Blanguages
%{_libdir}/%{name}/VERSION
%{_libdir}/%{name}/BlenderQuickStart.pdf
%{_libdir}/%{name}/blender.html
%{_libdir}/%{name}/copyright.txt
%{_libdir}/%{name}/release_%{relver}.txt
%{_libdir}/%{name}/scripts/*
%{_libdir}/%{name}/plugins/sequence
%{_libdir}/%{name}/plugins/texture
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}nodri.png
%{_liconsdir}/%{name}nodri.png
%{_iconsdir}/%{name}nodri.png
