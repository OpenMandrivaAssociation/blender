%define testver		248
%define	relver		248
%define name		blender
%define truename	blender
%define kde3altpath	/opt/kde3

%define build_debug     0
%{?_with_debug: %{expand: %%global build_debug 1}}
%{?_without_debug: %{expand: %%global build_debug 0}}

%define build_fullopt 1
%{?_with_fullopt: %{expand: %%global build_fullopt 1}}
%{?_without_fullopt: %{expand: %%global build_fullopt 0}}

%define build_profiling 0
%{?_with_profiling: %{expand: %%global build_profiling 1}}
%{?_without_profiling: %{expand: %%global build_profiling 0}}

%define build_systembullet 0
%{?_with_systembullet: %{expand: %%global build_systembullet 1}}
%{?_without_systembullet: %{expand: %%global build_systembullet 0}}

%define build_systemffmpeg 0
%{?_with_systemffmpeg: %{expand: %%global build_systemffmpeg 1}}
%{?_without_systemffmpeg: %{expand: %%global build_systemffmpeg 0}}

%define build_verse	1
%{?_with_verse: %{expand: %%global build_verse 1}}
%{?_without_verse: %{expand: %%global build_verse 0}}

%define build_gameeng	1
%{?_with_gameeng: %{expand: %%global build_gameeng 1}}
%{?_without_gameeng: %{expand: %%global build_gameeng 0}}

%define build_player	1
%{?_with_player: %{expand: %%global build_player 1}}
%{?_without_player: %{expand: %%global build_player 0}}

%define use_smp		1
%{?_with_smp: %global use_smp 1}
%{?_without_smp: %global use_smp 0}

%define use_protector	0
%{?_with_protector: %global use_protector 1}
%{?_without_protector: %global use_protector 0}

%define no_protector	0
%{?_with_noprotector: %global no_protector 1}
%{?_without_noprotector: %global no_protector 0}

%define avoid_dunno_patent	1
%{?_with_avoidpatent: %global avoid_dunno_patent 1}
%{?_without_avoidpatent: %global avoid_dunno_patent 0}

%if %{use_smp}
%define scons_smp --debug=time -j %(expr $(getconf _NPROCESSORS_ONLN) + 2)
%else
%define scons_smp %{nil}
%endif

%if %{use_protector}
%define protector_flags -fstack-protector -fstack-protector-all --param=ssp-buffer-size=1
%else
%define protector_flags %{nil}
%endif

%if %{no_protector}
%define protector_flags -fno-stack-protector
%else
%define protector_flags %{nil}
%endif

%if %{build_profiling}
%define profiling_flags	-Wall -g -pg
%else
%define profiling_flags %{nil}
%endif

%if %{build_systemffmpeg}
%define	ffmpeg_source '/usr'
%if %{mdkversion} <= 200810
%define ffmpeg_lib 'avformat avcodec avutil'
%else
%define ffmpeg_lib 'avformat avcodec swscale avutil'
%endif
%else
%define ffmpeg_source '\#extern/ffmpeg'
%define ffmpeg_lib ''
%endif

%if %{build_verse}
%define verse_bool 'true'
%else
%define verse_bool 'false'
%endif

%if %{build_gameeng}
%define gameeng_bool 'true'
%else
%define gameeng_bool 'false'
%endif

%if %{build_player}
%define player_bool 'true'
%else
%define player_bool 'false'
%endif

%define ffmpeg_bool 'true'
%define redcode_bool 'false'

%if %{mdkversion} <= 200610
%define opengl_libpath	'%{_prefix}/X11R6/%{_lib}'
%else
%define	opengl_libpath	'%{_libdir}'
%endif

%if %{mdkversion} >= 200800
%define openmp_bool 'true'
%else
%define openmp_bool 'false'
%endif

Name:		%{name}
Version:	2.48a
Release:	%mkrel 3
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
Patch1:		blender-2.48-libffmpeg-system.patch
Patch2:		blender-2.46-lib64.patch
Patch3:		blender-2.42-forceyafrayplug.patch
Patch4:		blender-2.46-libquicktime.patch
Patch10:	blender-2.48a-O3opt.patch
Patch13:	blender-2.48-python25.patch
Patch14:	blender-2.48-alut.patch
Patch17:	blender-2.48a-changelog.patch
Patch18:	blender-2.46-yafray_zero_threads.patch
Patch19:	blender-2.46-maxthreads.patch
Patch20:	blender-2.44-force-python24.patch
Patch21:	blender-2.44-boxpack2d-missed.patch
Patch22:	blender-2.46-bug6811.patch
Patch23:	blender-2.44-more-than-six-subsurf.patch
Patch24:	blender-2.45-import-dxf-logpath.patch
Patch34:	blender-2.48a-deinterlace.patch
Patch37:	blender-2.46-arith-optz.patch
Patch38:	blender-2.46-ffmpeg-new.patch
Patch39:	blender-2.46-scons-new.patch
# From Fedora: fix CVE-2008-1103-1 - AdamW 2008/09 #44196
Patch40:	blender-2.46rc3-cve-2008-1103-1.patch
# Disable x264, xvid and mp3lame support in blender's ffmpeg: these
# cannot be in the MDV repos for legal reasons - AdamW 2008/09
Patch41:	blender-2.48a-legal.patch
Patch42:	blender-2.48a-fix-str-fmt.patch
URL:		http://www.blender.org/
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	scons
%if %{mdkversion} >= 200810
BuildRequires:	python-scons
%endif
BuildRequires:	openal-devel >= 0.0.6-9mdk
%if %{mdkversion} >= 200810
BuildRequires:	OpenEXR-devel >= 1.6.1
%else
BuildRequires:	OpenEXR-devel
%endif
%if %{build_systembullet}
BuildRequires:	bullet-devel
%endif
BuildRequires:	esound-devel
%if %{mdkversion} >= 200700
BuildRequires:  freealut-devel
%endif
BuildRequires:	ffmpeg-devel >= 0.4.9-1.pre1
%if %{mdkversion} >= 200710
BuildRequires:	ffmpeg-devel >= 0.4.9-3.pre1.7407.10
%endif
BuildRequires:	ftgl-devel
BuildRequires:	gettext-devel
%if %{mdkversion} >= 200800
BuildRequires:	libgomp-devel
%endif
BuildRequires:	jpeg-devel
BuildRequires:	mesaglu-devel
#BuildRequires:	glew-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	openssl-devel
BuildRequires:	png-devel
BuildRequires:	python-devel >= 2.4
BuildRequires:	SDL-devel
BuildRequires:	smpeg-devel
BuildRequires:	%{mklibname tiff 3}-devel
BuildRequires:	X11-devel
BuildRequires:	yasm
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

Please note that the ability of Blender to export to h.264 and Xvid
video formats, and MP3 audio format, has been disabled in this build
due to patent issues.

%if %{build_debug}
This version is built with debug enabled.
%endif

%prep
%setup -q -n %{truename}-%{version} -a 2
%patch0 -p1 -b .openal
%if %{mdkversion} >= 200710
%patch1 -p1 -b .ffmpeg
%endif
%if "%{_lib}" != "lib"
%patch2 -p1 -b .lib64
%endif
%patch3 -p1 -b .yafray
#%patch4 -p1 -b .quicktime
%patch10 -p0 -b .O3opt
%if %{mdkversion} >= 200710
%patch13 -p1 -b .python
%else
%patch20 -p1 -b .python24
%endif
%if %{mdkversion} >= 200700
%patch14 -p1 -b .alut
%endif
%patch17 -p1 -b .chglog
%patch18 -p1 -b .zero_threads
%patch19 -p1 -b .maxthreads
%patch21 -p1
%patch22 -p0 -b .bug6811
%patch23 -p1 -b .subsurf
%patch34 -p1 -b .deinterlace
#%patch36 -p1 -b .outliner
%patch37 -p1 -b .optz
%if %{mdkversion} >= 200900 && %{build_systemffmpeg}
%patch38 -p1 -b .ffmpegnew
%endif
%patch39 -p1 -b .sconsnew
%patch40 -p1 -b .cve200811031
%if !%{build_systemffmpeg} && %{avoid_dunno_patent}
%patch41 -p1 -b .legal
%endif
%patch42 -p0 -b .str

# Fix pt_BR
sed -i "s,pt_br,pt_BR,g" bin/.blender/.Blanguages

%build
%if %{build_debug}
%define debug_flags -g
%define scons_debug BF_DEBUG=1
%else
%define debug_flags %{nil}
%define scons_debug BF_DEBUG=0
%endif

cat > user-config.py <<EOF
BF_GETTEXT_LIBPATH = '\${BF_GETTEXT}/%{_lib}'
WITH_BF_FFMPEG = %{ffmpeg_bool}
BF_FFMPEG = %{ffmpeg_source}
BF_FFMPEG_LIB = %{ffmpeg_lib}
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
WITH_BF_VERSE = %{verse_bool}
WITH_BF_GAMEENGINE = %{gameeng_bool}
WITH_BF_PLAYER = %{player_bool}
BF_OPENGL_LIBPATH = %{opengl_libpath}
WITH_BF_OPENMP = %{openmp_bool}
WITH_BF_REDCODE = %{redcode_bool}
%if %{build_systembullet}
BF_BULLET = '%{_prefix}'
BF_BULLET_INC = '\${BF_BULLET}/include/bullet'
BF_BULLET_LIB = 'bulletdynamics bulletcollision bulletmath'
%endif
#
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 -ffast-math -mmmx -msse -msse2 -mfpmath=sse %{debug_flags} -funsigned-char -fno-strict-aliasing %{protector_flags}".split()
CXXFLAGS = "%{optflags} -O3 -ffast-math -mmmx -msse -msse2 -mfpmath=sse %{debug_flags} -funsigned-char -fno-strict-aliasing %{protector_flags}".split()
REL_CFLAGS  = "-O3".split()
REL_CCFLAGS = "-O3".split()
%endif
%if %{build_profiling}
BF_PROFILE = 'true'
BF_PROFILE_FLAGS= "%{profiling_flags}".split();
%endif
EOF

cat > user-config.py.sse <<EOF
BF_GETTEXT_LIBPATH = '\${BF_GETTEXT}/%{_lib}'
WITH_BF_FFMPEG = %{ffmpeg_bool}
BF_FFMPEG = %{ffmpeg_source}
BF_FFMPEG_LIB = %{ffmpeg_lib}
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
WITH_BF_VERSE = %{verse_bool}
WITH_BF_GAMEENGINE = %{gameeng_bool}
WITH_BF_PLAYER = %{player_bool}
BF_OPENGL_LIBPATH = %{opengl_libpath}
WITH_BF_OPENMP = %{openmp_bool}
WITH_BF_REDCODE = %{redcode_bool}
%if %{build_systembullet}
BF_BULLET = '%{_prefix}'
BF_BULLET_INC = '\${BF_BULLET}/include/bullet'
BF_BULLET_LIB = 'bulletdynamics bulletcollision bulletmath'
%endif
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 -ffast-math -msse -mfpmath=sse %debug_flags %profiling_flags -funsigned-char -fno-strict-aliasing %{protector_flags}".split()
CXXFLAGS = "%{optflags} -O3 -ffast-math -msse -mfpmath=sse %debug_flags %profiling_flags -funsigned-char -fno-strict-aliasing %{protector_flags}".split()
REL_CFLAGS  = "-O3".split()
REL_CCFLAGS = "-O3".split()
%if %{build_profiling}
BF_PROFILE = 'true'
BF_PROFILE_FLAGS= "%{profiling_flags}".split();
%endif
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
		%{buildroot}%{_datadir}/ \
%if %{mdkversion} >= 200900
		%{buildroot}%{kde3altpath}/share/mimelnk/application/ \
%endif
		%{buildroot}%{_datadir}/mimelnk/application/

%if %{build_verse}
install -m 755 ./installdir/verse %{buildroot}%{_libdir}/%{name}/verse
%endif
%if %{build_player}
install -m 755 ./installdir/blenderplayer %{buildroot}%{_libdir}/%{name}/%{truename}player
ln -s %{_libdir}/%{name}/%{truename}player %{buildroot}%{_bindir}/%{name}player
%endif
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
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}fs.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}nodri.desktop << EOF
[Desktop Entry]
Name=Blender (DRI disabled)
Comment=The free open source 3D content creation suite (with DRI disabled)
Exec=%{_bindir}/%{name}nodri -w %f
Icon=%{name}nodri
Terminal=false
Type=Application
Categories=3DGraphics;Graphics;Viewer;
EOF

# mimelnk
cat > %{buildroot}%{_datadir}/mimelnk/application/x-_blender.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Type=MimeType
MimeType=application/x-blender
Icon=blender
Patterns=*.blend;*.BLEND;
Comment=Blender 3d format
EOF

%if %{mdkversion} >= 200900
cp -p %{buildroot}%{_datadir}/mimelnk/application/x-_blender.desktop \
	%{buildroot}%{kde3altpath}/share/mimelnk/application/
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
export EXCLUDE_FROM_STRIP=".*"
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database} 
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database} 
%endif

%files
%defattr(-,root,root)
%doc ChangeLog README doc/*.txt test%{testver}
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/mimelnk/application/x-_blender.desktop
%if %{mdkversion} >= 200900
%{kde3altpath}/share/mimelnk/application/x-_blender.desktop
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
