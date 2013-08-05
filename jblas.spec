Summary: Java bindings for BLAS
Name: jblas
Version: 1.2.3
Release: 2%{?dist}
License: BSD
Group: System Environment/Libraries
URL: http://jblas.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: https://github.com/mikiobraun/jblas/archive/jblas-1.2.3.tar.gz
Patch0: 0001-Try-to-load-libraries-directly-on-Linux.patch
Patch1: 0001-Makefile-always-create-directories-before-writing-to.patch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  ruby
BuildRequires:  gcc-gfortran

BuildRequires:  junit
BuildRequires:  atlas-devel

Requires:       jpackage-utils
Requires:       java

%description
Wraps BLAS (e.g. ATLAS) using generated code through JNI.
Allows Java programs to use the full power of ATLAS/Lapack
through a convenient interface.

Uninstalling generic atlas rpm and installing an
architecture-specific version of atlas (e.g. atlas-sse3),
is recommended.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -qn %{name}-%{name}-%{version}
rm -rf src/main/resources/lib/static
%patch0 -p1
%patch1 -p1

%build
libdir="$(cd "/usr/lib/$(gcc -print-multi-os-directory)"; pwd)"
export LC_ALL="en_US.utf8"
./configure --ptatlas --libpath="$libdir/atlas" --arch-flavor=sse
make %{?_smp_mflags} CFLAGS="%{optflags} -fPIC"
ant minimal-jar javadoc
rm -rf javadoc/src-html

%install

mkdir -p $RPM_BUILD_ROOT%{_jnidir}
cp jblas-minimal-%{version}*.jar $RPM_BUILD_ROOT%{_jnidir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}
cp -r javadoc $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}
install -pm 755 src/main/resources/lib/dynamic/Linux/*/sse/libjblas.so \
                $RPM_BUILD_ROOT%{_libdir}/%{name}/

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_jnidir}/%{name}.jar
%{_libdir}/%{name}
%doc COPYING AUTHORS RELEASE_NOTES

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon Aug 05 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.3-2
- Make /usr/lib64/jblas owned.

* Tue Jul 30 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.3-1
- Initial packaging.
