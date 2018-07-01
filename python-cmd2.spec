#
# Conditional build:
%bcond_with	doc	# build doc (broken)
%bcond_with	tests	# do perform "make test" (broken)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	cmd2 - a tool for building interactive command line applications in Python
Name:		python-cmd2
Version:	0.7.5
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/99/18/0bfe8240ffaebd28b1bce5a48170404e32bc1de6e640c8e7f37f1e522edb/cmd2-%{version}.tar.gz
# Source0-md5:	9f758f3a6a20f1220d60f6320bb839b3
URL:		https://pypi.python.org/pypi/cmd2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pyparsing >= 2.0.1
BuildRequires:	python-pyperclip
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mock
BuildRequires:	python3-pyparsing >= 2.0.1
BuildRequires:	python3-pyperclip
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
%endif
Requires:	python3-pyparsing >= 2.0.1
Requires:	python3-pyperclip
Requires:	python3-six
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cmd2 is a tool for building interactive command line applications in
Python. Its goal is to make it quick and easy for developers to build
feature-rich and user-friendly interactive command line applications.
It provides a simple API which is an extension of Python's built-in
cmd module. cmd2 provides a wealth of features on top of cmd to make
your life easier and eliminates much of the boilerplate code which
would be necessary when using cmd.

%package -n python3-cmd2
Summary:	cmd2 - a tool for building interactive command line applications in Python
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-cmd2
cmd2 is a tool for building interactive command line applications in
Python. Its goal is to make it quick and easy for developers to build
feature-rich and user-friendly interactive command line applications.
It provides a simple API which is an extension of Python's built-in
cmd module. cmd2 provides a wealth of features on top of cmd to make
your life easier and eliminates much of the boilerplate code which
would be necessary when using cmd.

%package apidocs
Summary:	API documentation for Python cmd2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona cmd2
Group:		Documentation

%description apidocs
API documentation for Pythona cmd2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona cmd2.

%prep
%setup -q -n cmd2-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:pytest}
%endif

%if %{with python3}
%py3_build %{?with_tests:pytest}

%if %{with doc}
%{__python3} setup.py build_sphinx
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-cmd2-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-cmd2-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-cmd2-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%{py_sitescriptdir}/cmd2.py*
%{py_sitescriptdir}/cmd2-%{version}-py*.egg-info
%{_examplesdir}/python-cmd2-%{version}
%endif

%if %{with python3}
%files -n python3-cmd2
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%{py3_sitescriptdir}/cmd2.py
%{py3_sitescriptdir}/__pycache__/*
%{py3_sitescriptdir}/cmd2-%{version}-py*.egg-info
%{_examplesdir}/python3-cmd2-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
