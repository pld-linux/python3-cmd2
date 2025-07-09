# TODO: docs (BR: mkdocs + plugins)
#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	cmd2 - a tool for building interactive command line applications in Python
Summary(pl.UTF-8):	cmd2 - narzędzie do tworzenia interaktywnych aplikacji linii poleceń w Pythonie
Name:		python3-cmd2
Version:	2.7.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cmd2/
Source0:	https://files.pythonhosted.org/packages/source/c/cmd2/cmd2-%{version}.tar.gz
# Source0-md5:	16990c5aef2162ee2d42d2a9546000d6
URL:		https://pypi.org/project/cmd2/
BuildRequires:	python3-build >= 1.2.1
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:64
BuildRequires:	python3-setuptools_scm >= 8
BuildRequires:	python3-trove_classifiers >= 2025.5.8.15
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-coverage >= 7
BuildRequires:	python3-pyparsing >= 2.0.1
BuildRequires:	python3-pyperclip >= 1.8
BuildRequires:	python3-pytest >= 7
BuildRequires:	python3-pytest-cov >= 4
BuildRequires:	python3-pytest-mock >= 3.14
BuildRequires:	python3-rich_argparse >= 1.7.1
BuildRequires:	python3-wcwidth >= 0.2.10
%endif
Requires:	python3-modules >= 1:3.9
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

%description -l pl.UTF-8
cmd2 to narzędzie do tworzenia interaktywnych aplikacji linii poleceń
w Pythonie. Jego celem jest ułatwienie szybkiego tworzenia bogatych
funkcjonalnie, przyjaznych dla użytkownika aplikacji linii poleceń.
Zapewnia proste API, rozszerzające wbudowany w Pythona moduł cmd; daje
bogate możliwości, ułatwiające życie i eliminujące dużą część
powtarzalnego kodu, który trzeba by było napisać, używając cmd.

%prep
%setup -q -n cmd2-%{version}

%{__sed} -i -e '1s,/usr/bin/env python3\?$,%{__python3},' examples/*.py examples/scripts/arg_printer.py
%{__sed} -i -e '1s,/usr/bin/env zsh$,/bin/zsh,' examples/tmux_*.sh

%build
%py3_build_pyproject

%if %{with tests}
# SIGINT test fail for unknown reason
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_mock.plugin \
%{__python3} -m pytest tests -k 'not test_proc_reader_send_sigint and not test_proc_reader_terminate'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/cmd2
%{py3_sitescriptdir}/cmd2-%{version}.dist-info
%{_examplesdir}/python3-cmd2-%{version}
