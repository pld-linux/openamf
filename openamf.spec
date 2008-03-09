#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
#
%include	/usr/lib/rpm/macros.java
%define		subver		RC12
%define		rel	0.1
Summary:	OpenAMF - Java Flash Remoting
Summary(pl.UTF-8):	OpenAMF - sterowanie flashem z poziomu Javy
Name:		openamf
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	LGPL v2.1
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/openamf/%{name}-%{version}%{subver}.zip
# Source0-md5:	de8096703da0853a1be6dc0148fec255
URL:		http://sourceforge.net/projects/openamf/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
BuildRequires:	jakarta-cactus
Requires:	jpackage-utils
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenAMF project is a free open-source alternative to Macromedia's
Java Flash Remoting. It is as capable of providing application
services to Flash MX as Macromedia's proprietary solution.

%description -l pl.UTF-8
Projekt OpenAMF to wolnodostępna, mająca otwarte źródła alternatywa
dla Java Flash Remoting Macromedii. Udostępnia usługi aplikacyjne dla
Flash MX takie jak rozwiązanie własnościowe Macromedii.

%package javadoc
Summary:	Online manual for OpenAMF
Summary(pl.UTF-8):	Dokumentacja Javadoc do OpenAMF
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc documentation for OpenAMF.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc do OpenAMF.

%description javadoc -l fr.UTF-8
Javadoc pour OpenAMF.

%prep
%setup -q -n %{name}-%{version}%{subver}
%{__sed} -i -e 's,\r$,,' changes.txt

%build
required_jars="
ant
aspectjrt
astranslator
axis
beanutils
cactus
cactus-ant
collections
commons-codec
commons-discovery
commons-httpclient
commons-lang
digester
digester-rss
httpunit
jaxrpc
junit
junit
log4j
logging
mysql-connector-java
saaj
servlet
spring
wsdl4j
"
export CLASSPATH=$(build-classpath $required_jars)
%ant -f build/build.xml jar %{?with_javadoc:javadoc}

#    <property name="ant.jar.file" value="${lib.dir}/ant.jar"/>
#    <property name="astranslator.jar.file" value="${lib.dir}/astranslator-1.5.9.jar"/>
#    <property name="axis.jar.file" value="${lib.dir}/axis.jar"/>
#    <property name="wsdl4j.jar.file" value="${lib.dir}/wsdl4j.jar"/>
#    <property name="jaxrpc.jar.file" value="${lib.dir}/jaxrpc.jar"/>
#    <property name="commons-discovery.jar.file" value="${lib.dir}/commons-discovery.jar"/>
#    <property name="saaj.jar.file" value="${lib.dir}/saaj.jar"/>
#    <property name="mysql.jar.file" value="${lib.dir}/mysql-connector-java-3.0.6-stable-bin.jar"/>
#    <property name="log4j.jar.file" value="${lib.dir}/log4j-1.2.9.jar"/>
#    <property name="logging.jar.file" value="${lib.dir}/commons-logging-1.0.4.jar"/>
#    <property name="beanutils.jar.file" value="${lib.dir}/commons-beanutils-1.7.0.jar"/>
#    <property name="collections.jar.file" value="${lib.dir}/commons-collections-3.1.jar"/>
#    <property name="digester.jar.file" value="${lib.dir}/commons-digester.jar"/>
#    <property name="digester-rss.jar.file" value="${lib.dir}/commons-digester-rss.jar"/>
#    <property name="lang.jar.file" value="${lib.dir}/commons-lang-2.1.jar"/>
#    <property name="spring.jar.file" value="${lib.dir}/spring.jar"/>
#    <property name="httpclient.jar.file" value="${lib.dir}/commons-httpclient-3.0.jar"/>
#    <property name="commons-codec.jar.file" value="${lib.dir}/commons-codec-1.3.jar"/>
#    <property name="junit.jar.file" value="${lib.dir}/junit-3.8.1.jar"/>


#        <include name="junit-3.8.1.jar"/>
#        <include name="aspectjrt-1.1.1.jar"/>
#        <include name="cactus-1.5.jar"/>
#        <include name="cactus-ant-1.5.jar"/>
#        <include name="httpunit-1.5.3.jar"/>


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
# install jar
cp -a dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README.txt changes.txt
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
