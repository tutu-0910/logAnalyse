#!/bin/sh

git log  --after="$1"  --oneline  | wc -l

exit 0
