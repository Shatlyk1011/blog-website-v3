#!/usr/bin/env sh

set -eu

HUGO_VERSION="0.167.0"
PAGEFIND_VERSION="1.5.2"
BUILD_TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_TEMP_DIR"' EXIT

curl -fsSL -o "$BUILD_TEMP_DIR/hugo.tar.gz" \
  "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
tar -xzf "$BUILD_TEMP_DIR/hugo.tar.gz" -C "$BUILD_TEMP_DIR"

"$BUILD_TEMP_DIR/hugo" --gc --minify

# Pagefind indexes Hugo's completed output, so it must run after Hugo on every
# deployment. The generated public/pagefind directory is intentionally not
# committed; Vercel serves the freshly generated assets from this build.
curl -fsSL -o "$BUILD_TEMP_DIR/pagefind.tar.gz" \
  "https://github.com/Pagefind/pagefind/releases/download/v${PAGEFIND_VERSION}/pagefind-v${PAGEFIND_VERSION}-x86_64-unknown-linux-musl.tar.gz"
tar -xzf "$BUILD_TEMP_DIR/pagefind.tar.gz" -C "$BUILD_TEMP_DIR"

"$BUILD_TEMP_DIR/pagefind" --site public
