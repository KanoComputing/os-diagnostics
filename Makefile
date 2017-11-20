#
# Makefile
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#
# Build file for the diagnostics tool
#
# To build for deployment, the Python Pip module nuitka is required:
#     pip install nuitka
#


all: diagnostics

.PHONY:

diagnostics: .PHONY
	nuitka --standalone ./bin/diagnose
