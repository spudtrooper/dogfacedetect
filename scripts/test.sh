#!/bin/sh

set -e

scripts=$(dirname $0)

input_dir="testdata/glob"
output_dir="test-output/multithreaded"
rm -rf "$output_dir"
mkdir -p "$output_dir"

args=(
  -vvvv
  --input_dir="$input_dir"
  --output_dir="$output_dir"
  --multithreaded
  file-that-does-not-exist
  testdata/explicit/4.png
)
$scripts/run.sh "${args[@]}" "$@"

input_dir="testdata/glob"
output_dir="test-output/sync"
rm -rf "$output_dir"
mkdir -p "$output_dir"

args=(
  -vvvv
  --input_dir="$input_dir"
  --output_dir="$output_dir"
  file-that-does-not-exist
  testdata/explicit/4.png
)
$scripts/run.sh "${args[@]}"  "$@"