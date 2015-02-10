#!/bin/bash

set -o errexit

function usage {
echo "Usage: $0 [OPTION]..."
echo "Run Horizon's test suite(s)"
echo ""
echo "  -h, --help               Print this usage message"
echo "  -p, --pep8               Just run pep8"
exit
}

function process_option {
case "$1" in
  -h|--help) usage;;
  -p|--pep8) pep8=1;;
esac
}

function run_pep8 {
echo "Running pep8..."
pep8 --exclude venv .
}

pep8=0

for arg in "$@"; do
  process_option $arg
done

if [ $pep8 -eq 1 ]; then
  run_pep8
  exit
fi
