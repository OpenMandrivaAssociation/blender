Name:		blender
Version:	2.57b
Release:	%mkrel 1
Summary:	A fully functional 3D modeling/rendering/animation package
Group:		Graphics
Source0:	http://download.blender.org/source/blender-%{version}.tar.gz
Patch0:		blender-2.57-localedir.patch
Patch1:		blender-2.57-error-when-missing-sse.patch
Patch2:		blender-2.57-static-lib.patch
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
BuildRequires:	python3-devel >= 3.2

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
for i in 16x16 22x22 32x32 48x48 64x64 96x96 128x128 192x192 ; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}/apps
  install -pm 0644 release/freedesktop/icons/${i}/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm 0644 release/freedesktop/icons/scalable/%{name}.svg \
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
   %{_gconftool_bin} --type boolean --set /desktop/gnome/thumbnailers/application@x-blender/enable true
   %{_gconftool_bin} --type string --set /desktop/gnome/thumbnailers/application@x-blender/command "blender-thumbnailer.py %u %o"
fi

%preun
if [ "$1" = "0" -a -x %{_gconftool_bin} ]; then
   %{_gconftool_bin} --unset /desktop/gnome/thumbnailers/application@x-blender/enable
   %{_gconftool_bin} --unset /desktop/gnome/thumbnailers/application@x-blender/command
fi

%files -f %name.lang
%defattr(-,root,root)
%doc release/text/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_datadir}/pixmaps/blender.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
