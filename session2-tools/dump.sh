#!/bin/bash
# usage: dump.sh <rootdir> <subpath-filter> <outfile>
root=$1; filt=$2; out=$3
cd "$root"
find $filt -name '*.class' | sed 's/\.class$//' | sort > /tmp/_cls_$$.txt
: > "$out"
split -l 60 /tmp/_cls_$$.txt /tmp/_chunk_$$_
for f in /tmp/_chunk_$$_*; do
  javap -p -c -cp . $(cat $f) >> "$out" 2>&1
done
rm -f /tmp/_chunk_$$_* /tmp/_cls_$$.txt
