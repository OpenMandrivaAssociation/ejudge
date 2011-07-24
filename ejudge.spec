%define ejudge_user ejudge
%define ejudge_group judges
%define ejudge_home /var/lib/ejudge
%define cgi_bin_dir /var/www/cgi-bin
%define httpd_htdocs_dir /var/www/html
%define ejudge_socket_dir /var/run/ejudge
%define lang_config_dir %_sysconfdir/ejudge/lang.d

Name: ejudge
Version: 2.3.18
Release: %mkrel 3

Summary: Ejudge is a programming contest managment system
License: GPL
Group: System/Servers
Url: http://www.ejudge.ru

# SVN:  https://unicorn.cmc.msu.ru/svn/ejudge/trunk/ejudge/ 
Source0: %name-svn6283.tar.bz2
Source1: %name.rc
Source2: ejudge-install.sh
Source5: ejudge-cntsguide.pdf
Source6: ejudge-refmanual.pdf

Patch1: ejudge-stylecheck.patch
Patch2: ejudge-tsc.c.patch
Patch3: ejudge-fpc-version.patch

BuildRequires: flex, sed, mktemp, libexpat-devel, zlib-devel, libzip-devel, libncursesw-devel, libmysql-devel

Requires: sharutils, httpd, e2fsprogs, php-iconv, gawk, sendmail
#Requires for compilers
Requires: kumir fpc libstdc++-static-devel glibc-static-devel

%description
Ejudge is a programming contest managment system.

%package doc
Summary: Documentation for ejudge
Group: System/Servers
Requires: %name = %version-%release
BuildArch: noarch

%description doc
User and contest administrator manual for ejudge system.

%prep
%setup -q -n ejudge
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp %SOURCE2 %SOURCE5 %SOURCE6 .

bzip2 -9k ChangeLog NEWS NEWS.RUS

%build

%configure                                                                \
--enable-charset=utf-8                                                    \
--enable-socket-path=%ejudge_socket_dir/userlist-socket                   \
--enable-super-serve-socket=%ejudge_socket_dir/super-serve-socket         \
--enable-new-server-socket=%ejudge_socket_dir/new-server-socket           \
--enable-contests-home-dir=%ejudge_home                                   \
--enable-local-dir=%ejudge_socket_dir				                  \
--libexec=%_libexecdir                                                    \
--enable-cgi-bin-dir=%_libexecdir/%name/cgi-bin                           \
--enable-conf-dir=%ejudge_home/data                                       \
--enable-cgi-conf-dir=../cgi-data                                         \
--enable-hidden-server-bins                                               \
--with-httpd-cgi-bin-dir=%cgi_bin_dir                                     \
--with-httpd-htdocs-dir=%httpd_htdocs_dir                                 \
--enable-ajax                                                             \
--enable-lang-config-dir=%lang_config_dir

%make RELEASE=1

%install
%make_install DESTDIR=%buildroot install
install -p -m755 -D %SOURCE1 %buildroot%_initddir/%name
install -d %buildroot%ejudge_home
install -d %buildroot%ejudge_socket_dir
install -d %buildroot%lang_config_dir
%find_lang %name

%pre
%_sbindir/groupadd -r -f %ejudge_group || :
%_sbindir/useradd -g %ejudge_group -c 'Ejudge server' -d %ejudge_home -r %ejudge_user || :
%_sbindir/usermod -a -G mail %ejudge_user

%post
%post_service ejudge

%preun
%preun_service ejudge
%_sbindir/userdel %ejudge_user -rf

%files -f %name.lang
%_sysconfdir/ejudge
%attr(2775,%ejudge_user,%ejudge_group) %dir %ejudge_home
%_initddir/%name
%_bindir/*
%_includedir/*
%_libdir/libchecker*
%_libexecdir/%name
%_datadir/%name
%doc AUTHORS ChangeLog.bz2 NEWS.bz2 NEWS.RUS.bz2 ejudge-install.sh

%files doc
%doc ejudge-*.pdf
