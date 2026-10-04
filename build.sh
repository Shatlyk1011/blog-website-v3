#!/usr/bin/env sh

set -eu

HUGO_VERSION="0.167.0"
BUILD_TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_TEMP_DIR"' EXIT

git submodule update --init --recursive

curl -fsSL -o "$BUILD_TEMP_DIR/hugo.tar.gz" \
  "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
tar -xzf "$BUILD_TEMP_DIR/hugo.tar.gz" -C "$BUILD_TEMP_DIR"

"$BUILD_TEMP_DIR/hugo" --gc --minify --destination "$PWD/public"
test -s "$PWD/public/index.html"
printf '%s\n' 'Verified generated file: public/index.html'
