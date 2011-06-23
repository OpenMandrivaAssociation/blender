Name:		blender
Version:	2.58
Release:	%mkrel 1
Summary:	A fully functional 3D modeling/rendering/animation package
Group:		Graphics
Source0:	http://download.blender.org/source/blender-%{version}.tgz
Source1:	ru.po
Patch0:		blender-2.58-localedir.patch
Patch1:		blender-2.57-error-when-missing-sse.patch
Patch2:		blender-2.58-static-lib.patch
# Patch from SuSe
Patch4:         blender-2.48-python64.patch
Patch5:         blender-2.48-undefine-operation.patch
# Patch submitted upstream - Blender Patches item #19234,
Patch6:         blender-2.50-uninit-var.patch
Patch7:         blender-2.55-gcc46fix.patch
# FIXME The following three patches revert blender to build with python 3.1
Patch10:         blender-2.56-svn35386.patch
Patch11:         blender-2.56-svn35395.patch
Patch12:         blender-2.57b-PYC_INTERPRETER_ACTIVE.patch

URL:		http://www.blender.org/
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	cmake >= 2.8
BuildRequires:	ffmpeg-devel
BuildRequires:	glew-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	SDL-devel
BuildRequires:	libx11-devel
BuildRequires:	libxi-devel
BuildRequires:	freetype2-devel
BuildRequires:	libgomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	openjpeg-devel
BuildRequires:	openal-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	sndfile-devel
BuildRequires:	tiff-devel
%if %mdvver >= 201100
BuildRequires:	python3-devel >= 3.2
%else
BuildRequires:	python3-devel
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
%setup -qn %{name}-%{version}
%patch0 -p0 -b .localedir
%patch1 -p0 -b .sse
%patch2 -p0 -b .static
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
#%patch8 -p0
%if %mdvver < 201100
%patch10 -p0
%patch11 -p0
%patch12 -p0
%endif

rm -f po/ru.po
cp -f %SOURCE1 po/ 

%build
%ifarch %{ix86}
# build non-sse flavour
%cmake -DWITH_INSTALL_PORTABLE=OFF -DWITH_PLAYER=ON \
	-DWITH_PYTHON=ON -DWITH_PYTHON_INSTALL=OFF \
	-DWITH_BUILTIN_GLEW=OFF \
	-DWITH_CODEC_FFMPEG=ON -DWITH_CODEC_SNDFILE=ON \
	-DWITH_RAYOPTIMIZATION=OFF
%make
cd ..
mv build non-sse
%endif

#build sse flavour
%cmake -DWITH_INSTALL_PORTABLE=OFF -DWITH_PLAYER=ON \
	-DWITH_PYTHON=ON -DWITH_PYTHON_INSTALL=OFF \
	-DWITH_BUILTIN_GLEW=OFF \
	-DWITH_CODEC_FFMPEG=ON -DWITH_CODEC_SNDFILE=ON \
	-DWITH_RAYOPTIMIZATION=ON
%make

%install
rm -rf %{buildroot}

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
mv %buildroot%_bindir/%name %buildroot%_bindir/%name.sse

#install non-sse flavour
rm -fr build
mv non-sse build
%makeinstall_std -C build
mv %buildroot%_bindir/%name %buildroot%_bindir/%name.nonsse

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

%find_lang %name

%clean
rm -rf %{buildroot}

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

%files -f %name.lang
%defattr(-,root,root)
%doc release/text/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
