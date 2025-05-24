#
# Conditional build:
%bcond_with	tests	# unit tests (some failing)

Summary:	cmd2 - a tool for building interactive command line applications in Python
Summary(pl.UTF-8):	cmd2 - narzędzie do tworzenia interaktywnych aplikacji linii poleceń w Pythonie
Name:		python3-cmd2
Version:	2.5.11
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cmd2/cmd2-%{version}.tar.gz
# Source0-md5:	8d5f8d668772c418e0e55942a2adcd8b
URL:		https://pypi.org/project/cmd2/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-pyparsing >= 2.0.1
BuildRequires:	python3-pyperclip
BuildRequires:	python3-pytest
BuildRequires:	python3-six
BuildRequires:	python3-wcwidth
%endif
Requires:	python3-modules >= 1:3.8
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

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      examples/arg_decorators.py \
      examples/basic.py \
      examples/default_categories.py \
      examples/dynamic_commands.py \
      examples/initialization.py \
      examples/modular_commands_basic.py \
      examples/modular_commands_dynamic.py \
      examples/modular_subcommands.py \
      examples/subcommands.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+zsh(\s|$),#!/bin/zsh\1,' \
      examples/tmux_launch.sh \
      examples/tmux_split.sh

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-cmd2-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/cmd2
%{py3_sitescriptdir}/cmd2-%{version}.dist-info
%{_examplesdir}/python3-cmd2-%{version}
