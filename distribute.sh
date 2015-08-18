#!/bin/bash
# distribute.sh
# Prepare project for AUR distribution.

build() {
  waf --package clean build --targets=PKGBUILD,mksrcinfo,.SRCINFO
}

if ! build 2>/dev/null; then
  # Only configure if not yet done.
  waf configure
  build
fi

builddir="$(grep -Po "(?<=out_dir = ').*(?=')" .lock-waf_linux_build)"
aurbranch -p "$builddir/PKGBUILD" -i "$builddir/.SRCINFO" wscript:
