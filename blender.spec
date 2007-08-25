%define testver		244
%define	relver		244
%define name		blender
%define truename	blender
%define svnsnapshot	20070724

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
%define scons_smp ""
%endif

Name:		%{name}
Version:	2.44
Release:	3.%{svnsnapshot}.%mkrel 2
Summary:	A fully functional 3D modeling/rendering/animation package
Group:		Graphics
Source0:	http://download.blender.org/source/blender-%{version}-%{svnsnapshot}-stable.tar.bz2
Source1: 	blender-wrapper
Source2:	http://download.blender.org/demo/test/test%{testver}.zip
Source11:	blender-16x16.png
Source12:	blender-32x32.png
Source13:	blender-48x48.png
Source14:	blendernodri-16x16.png
Source15:	blendernodri-32x32.png
Source16:	blendernodri-48x48.png
Patch0:		blender-2.41-openal-fix.patch
Patch1:		blender-2.42-buildfix.patch
Patch2:		blender-2.43-lib64.patch
Patch3:		blender-2.42-forceyafrayplug.patch
Patch5:		blender-2.41-libtiff.patch
Patch7:		blender-2.43-varuninitial.patch
Patch8:		blender-2.41-yafray-64.patch
Patch9:		blender-2.42-yafray-ncpus.patch
Patch10:	blender-2.42-O3opt.patch
Patch11:	blender-2.42a-morethreads.patch
Patch13:	blender-2.44-python25.patch
Patch14:	blender-2.44-alut.patch
Patch16:	blender-2.43-rc3-avclose.patch
Patch17:	blender-2.44-changelog.patch
Patch18:	blender-2.43-yafray_zero_threads.patch
Patch19:	blender-2.43-maxthreads.patch
Patch20:	blender-2.44-force-python24.patch
Patch21:	blender-2.44-boxpack2d-missed.patch
Patch22:	blender-2.44-bug6811.patch
URL:		http://www.blender.org/
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	scons
BuildRequires:	openal-devel >= 0.0.6-9mdk
BuildRequires:	OpenEXR-devel
BuildRequires:	esound-devel
BuildRequires:  freealut-devel
BuildRequires:	ffmpeg-devel >= 0.4.9-3.pre1.7407.10
BuildRequires:	ftgl-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	mesaglu-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	openssl-devel
BuildRequires:	png-devel
BuildRequires:	python-devel >= 2.4
BuildRequires:	SDL-devel
BuildRequires:	smpeg-devel
BuildRequires:	%{mklibname tiff 3}-devel
BuildRequires:	XFree86-devel
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
%patch13 -p1 -b .python
%patch14 -p1 -b .alut
%patch16 -p1 -b .imgbro
%patch17 -p1 -b .chglog
%patch18 -p1 -b .zero_threads
%patch19 -p1 -b .maxthreads
%patch21 -p1
%patch22 -p1 -b .bug6811

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
WITH_BF_FFMPEG = 'true'
WITH_BF_VERSE = 'true'
WITH_BF_GAMEENGINE = 'true'
WITH_BF_PLAYER = 'true'
#WITH_BF_ODE = 'true'
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
BF_OPENGL_LIBPATH = '%{_prefix}/X11R6/%{_lib}'
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 %debug_flags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -ffast-math -funsigned-char -fno-strict-aliasing".split()
CXXFLAGS = "%{optflags} -O3 %debug_flags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -ffast-math -funsigned-char -fno-strict-aliasing".split()
REL_CFLAGS  = "-O3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE".split()
REL_CCFLAGS = "-O3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE".split()
%endif
EOF

cat > user-config.py.sse <<EOF
BF_GETTEXT_LIBPATH = '\${BF_GETTEXT}/%{_lib}'
WITH_BF_FFMPEG = 'true'
WITH_BF_VERSE = 'true'
WITH_BF_GAMEENGINE = 'true'
WITH_BF_PLAYER = 'true'
#WITH_BF_ODE = 'true'
BF_FFMPEG_LIBPATH = '\${BF_FFMPEG}/%{_lib}'
BF_OPENGL_LIBPATH = '%{_prefix}/X11R6/%{_lib}'
BF_BUILDDIR = './builddir'
BF_INSTALLDIR = './installdir'
%if %{build_fullopt}
CCFLAGS  = "%{optflags} -O3 %debug_flags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -ffast-math -msse -mfpmath=sse -funsigned-char -fno-strict-aliasing".split()
CXXFLAGS = "%{optflags} -O3 %debug_flags -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -ffast-math -msse -mfpmath=sse -funsigned-char -fno-strict-aliasing".split()
REL_CFLAGS  = "-O3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE".split()
REL_CCFLAGS = "-O3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE".split()
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
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): command="%{_bindir}/%{name} -w" \
	needs="X11" \
	icon="%{name}.png" \
	section="Multimedia/Graphics" \
	title="Blender" \
	longtitle="A fully functional 3D modeling/rendering/animation package" \
	xdg="true" \
	mimetypes="application/x-blender"
EOF
cat > %{buildroot}%{_menudir}/%{name}fs <<EOF
?package(%{name}): command="%{_bindir}/%{name} -W" \
	needs="X11" \
	icon="%{name}.png" \
	section="Multimedia/Graphics" \
	title="Blender (FullScreen)" \
	xdg="true" \
	longtitle="A fully functional 3D modeling/rendering/animation package (in FullScreen mode)"
EOF
cat > %{buildroot}%{_menudir}/%{name}nodri <<EOF
?package(%{name}): command="%{_bindir}/%{name}nodri -w" \
	needs="X11" \
	icon="%{name}nodri.png" \
	section="Multimedia/Graphics" \
	title="Blender (No DRI)" \
	xdg="true" \
	longtitle="A fully functional 3D modeling/rendering/animation package (with DRI disabled)"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Blender
Comment=The free open source 3D content creation suite
Exec=%{_bindir}/%{name} -w %f
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics/Photography/3DGraphics;Graphics;Viewer;
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
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics/Photography/3DGraphics;Graphics;Viewer;
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
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics/Photography/3DGraphics;Graphics;Viewer;
EOF

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
%{update_desktop_database} 

%postun
%{clean_menus}
%{clean_desktop_database} 

%files
%defattr(-,root,root)
%doc ChangeLog README doc/*.txt test%{testver}
%{_bindir}/*
%{_menudir}/*
%{_datadir}/applications/*
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


%changelog
* Sat Aug 04 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.44-3.20070724.2mdv2007.1
- Added patch for blender bug 6811.
- Added verse binaries.

* Sat Jul 21 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.44-3.20070721.1mdv2007.1
- Branch stable 2.44 of 20070721.
- Updated Patch17.

* Mon May 14 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.44-2mdv2008.0
+ Revision: 26720
- Added Patch21, for missed boxpack2d.py script (still needed by
  some other scripts).

* Sun May 13 2007 Giuseppe Ghibò <ghibo@mandriva.com> 1mdv2008.0-current
+ Revision: 26582
- Release: 2.44.
- Removed Patch15, now 64bit is officially supported.
- Enabled Verse.

* Sun May 13 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-4mdv2008.0
+ Revision: 26575
- Fixed Patch18 for zero threads (bug #30137).
- Added Patch19 to allow 16 threads.


* Wed Mar 14 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-3mdv2007.1
+ Revision: 143270
- Rebuilt against latest ffmpeg.
- Ensure Building with against ffmpeg containing the img_convert in the API.
- Added Patch18 to avoid yafray rendering with 0 threads.

* Sat Feb 17 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-1mdv2007.1
+ Revision: 122138
- Enabled smp for building.
- Rebuilt Patch7.
- Removed Patch12, merged upstream.
- Updated Source0.
- Removed old Sources from tree.
- 2.43 final.
- Added Patch17 for fixing ChangeLog.
- Readded Patch16.
- Added InitialPreference in .desktop files.
- 2.43-20070214 (>RC3).
- use %%{name} macro to allow future build with version in name.

* Thu Feb 08 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070207.2mdv2007.1
+ Revision: 117805
- Added Patch16 for fixing segfault in Image Browser.

* Wed Feb 07 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070207.1mdv2007.1
+ Revision: 117069
- 2.43-20070707 (RC3).

* Sun Jan 28 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070128.1mdv2007.1
+ Revision: 114624
- release cvs 20070128 (>2.43RC2).
- call executable with -w (bug #26454).
- fixed blenderplayer position to correctly save the runtime.

* Fri Jan 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070119.1mdv2007.1
+ Revision: 110976
- Release 20070119 from CVS.
- Added Patch15 for 64bit warning.

* Fri Jan 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070118.1mdv2007.1
+ Revision: 110554
- Release 20070118 from CVS.
- Removed Patch15 (no longer needed).

* Sun Jan 07 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.43-0.20070101.2mdv2007.1
+ Revision: 105281
- modified string size in Patch12 to 16 to preserve the ABI.
- conditional BuildRequires for freealut-devel.
- Release 20070101 from CVS (RC1).
- Rebuilt Patch2.
- Rebuilt Patch12.
- Added freealut to Buildrequires (from Jan Ciger).
- Reworked Patch13 and Patch14 (from Jan Ciger) and apply
  only for 2007.1 (since python-config command was
  not available into python 2.4 package).
- Added Patch15 for fixing buffer overflow over stronger
  optimization flags.

* Wed Aug 23 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.42a-3mdv2007.0
+ Revision: 57087
- Fixed buffer overflow of bug #24583.

* Thu Aug 10 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.42a-2mdv2007.0
+ Revision: 54796
- Added Patch11 for to allow more threads.

  + Olivier Blin <oblin@mandriva.com>
    - fix typo in wrapper script, when upgrading from a previous version

* Sun Jul 30 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.42a-1mdv2007.0
+ Revision: 42619
- Release 2.42a.

* Tue Jul 25 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.42-2mdv2007.0
+ Revision: 41974
- changed ffmpeg-devel BuildRequires to 0.4.9-1.pre1.
- added OpenEXR-devel to BuildRequires
- added version into ffmpeg-devel BuildRequires and
  conditional switch (for MDV2006, since older ffmpeg, the
  ffmpeg support will be disabled).
- set mode 644 for internal .py scripts.
- use %%update_desktop_database instead of %%clean_desktop_database
  in %%post.
- xdg menus.
- fixes to wrapper.
- disabled -ftree-vectorize from CFLAGS, CXXFLAGS as it doesn't give
  improvements in rendering time.
- clean CFLAGS, CXXFLAGS.
- correctly copy user-config.py.std to user-config.py
- fixed install path of blender.sse.
- fixed cp of blender.sse.
- added blender-2.42-buildfix.patch.
- Added Patch10 for fixing problems with -O3 optimization
- Added Patch9 for fixing problem with SMP and yafray.
- Improved regexp for blendernodri (thanks to blino).
- Readapted Patch2,3.
- Removed Patch4,6  (merged upstream).
- fix applying Patch9
- fix minimal number of cpus/threads when called yafray.
- Better patch for x86-64
- added patch for correctly searching yafray plugin
- Added Requires: libtiff (dinamically loaded).
- Added Patch5 for loading libtiff.so.3 instead of libtiff.so (avoid
  installation of libtiff devel package).
- Added Patch6 for fixing a missed header.
- Added Patch7 for fixing an unitialized variable.
- [$VER: 2.41-5mdv]
- Force calling yafray trough library and not trough XML file (Patch3) as
  XML doesn't work anymore with yafray > 0.07, and anyway plugin it's better.
- Added yafray in Requires.
- Quote \$@ in wrapper.
- Added blendernodri wrapper to avoid blender's UI flashing problems
  with some card under DRI (e.g. Matrox).
- Updated svg2obj python script to 0.47.

  + Helio Chissini de Castro <helio@mandriva.com>
    - Fixed the mess did on svn versus regular upload. We should take more care in
      further operations.
      * Seg Mai 22 2006 Giuseppe Ghib?\195?\178 <ghibo@mandriva.com> 2.41-3mdk
    - Stronger optimization with %%optflags (thanks to Pixel).
    - python-devel >= 2.4 in BuildRequires.
    - New wrapper. Blender plugins usually deal with a lot of tmp/inplace writing.
      So now user get their own .blender env created.
    - Fixed locale translations.
    - Fixed pt_BR potfile naming
    - New upstream release
    - Finally we have blender internationalized, ann compiling in x86_64
    - Physics engine ODE isn't compiling at this moment
    - blenderplayer was reenabled, so game on again :-)
    - Still fixing my mess
    - Fix my mess

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Fri Apr 14 2006 Giuseppe Ghib� <ghibo@mandriva.com> 2.40-2mdk
- Added tiff-devel to BuildRequires.

* Wed Dec 28 2005 Olivier Blin <oblin@mandriva.com> 2.40-1mdk
- New release 2.40

* Thu Aug 04 2005 Gustavo Pichorim Boiko <boiko@mandriva.com> 2.37a-1mdk
- Updated to version 2.37a
- Added blenderplayer (the standalone game player)
- Added some default python scripts for importing and exporting
- Added localization files to the package. They were put into the main package
  because blender doesn't automatically choose the language in the interface.

* Fri Jun 03 2005 Olivier Blin <oblin@mandriva.com> 2.37-1mdk
- 2.37 : http://www.blender3d.org/cms/Blender_2_37.496.0.html

* Fri Dec 24 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.36-1mdk
- 2.36

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.35-2mdk
- Rebuild for new python

* Tue Nov 16 2004 Olivier Blin <blino@mandrake.org> 2.35-1mdk
- 2.35 : http://www.blender3d.org/cms/Blender_2_35.482.0.html

* Sat Aug 07 2004 Olivier Blin <blino@mandrake.org> 2.34-1mdk
- 2.34 : http://www.blender3d.org/cms/Blender_2_34.319.0.html
- remove gcc/libstdc++ patches (fixed upstream)
- fix doc files list

* Thu Jun 24 2004 Olivier Blin <blino@mandrake.org> 2.33a-1mdk
- 2.33a (yeah, game engine is back)
- rediff Patch1
- more gcc 3.4 template fixes (Patch2)
- switch to scons build system

* Thu Jun 17 2004 Olivier Blin <blino@mandrake.org> 2.32-2mdk
- rebuilt for new libstdc++
- Added Patch0 to fix build with new libstdc++
- Added Patch1 to fix build with gcc 3.4

* Sat Apr 03 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.32-1mdk
- 2.32
- fix buildrequires (lib64..)
- don't bzip2 icons in src.rpm

