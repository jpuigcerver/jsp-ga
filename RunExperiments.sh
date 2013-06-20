#!/bin/bash
set -e
export LC_NUMERIC=C

IDIR=Instances/S
REFS=Small_Results_Reference.txt
REPS=10
PS=50
IT=1000
CP=1.0
MP=0.05

function usage () {
    cat <<EOF
Usage: $0 [OPTIONS]
Options:
  -h
  -d <inst-dir>        Instances directory: "$IDIR"
  -t <ref-file>        Reference file: "$REFS"
  -r <repetitions>     Execution repetitions for each instance: $REPS
  -p <population>      Population size. Current: $PS
  -i <iterations>      Number of iterations. Current: $IT
  -c <crossover-prob>  Crossover probability. Current: $CP
  -m <mutation-prob>   Mutation probability. Current: $MP
EOF
}

while [ "$1" != "" ]; do
    case "$1" in
	"-h")
	    usage;
	    exit 0
	    ;;
	"-d")
	    IDIR="$2";
	    shift 2;
	    ;;
	"-t")
	    REFS="$2";
	    shift 2;
	    ;;
	"-r")
	    REPS=$2;
	    shift 2;
	    ;;
	"-p")
	    PS=$2;
	    shift 2;
	    ;;
	"-i")
	    IT=$2;
	    shift 2;
	    ;;
	"-c")
	    CP=$2;
	    shift 2;
	    ;;
	"-m")
	    MP=$2;
	    shift 2;
	    ;;
	*)
	    echo "Unknown option: $1" >&2;
	    usage;
	    exit 1;
    esac
done

FILES=( `find "$IDIR" -name "*.txt"` )

glob_nbest=0; glob_nequa=0; glob_nwors=0;
glob_sum_diff=0.0; glob_sum_sq_diff=0.0;
for f in ${FILES[@]}; do
    bf=`basename $f`
    ref_ts=`grep $bf $REFS | awk '{print $2}'`
    sum_ts=0.0; sum_sq_ts=0.0;
    sum_diff=0.0; sum_sq_diff=0.0;
    nbest=0;nequa=0;nwors=0;
    min_ts=1000000000000;
    for r in `seq 1 $REPS`; do
	out=`python jsp.py -s $RANDOM -i $IT -p $PS -c $CP -m $MP $f`
	[ $? -ne 0 ] && { exit 1; }
	ts=`echo "$out" | awk '{print $1}'`
	diff=`echo "$ref_ts - $ts" | bc -l`
	sum_ts=`echo "$sum_ts + $ts" | bc -l`
	sum_sq_ts=`echo "$sum_sq_ts + $ts * $ts" | bc -l`
	sum_diff=`echo "$sum_diff + $diff" | bc -l`
	sum_sq_diff=`echo "$sum_sq_diff + $diff * $diff" | bc -l`
	glob_sum_diff=`echo "$glob_sum_diff + $diff" | bc -l`
	glob_sum_sq_diff=`echo "$glob_sum_sq_diff + $diff * $diff" | bc -l`
	[ $ts -lt $ref_ts ] && { nbest=$[nbest + 1]; glob_nbest=$[glob_nbest + 1]; }
	[ $ts -eq $ref_ts ] && { nequa=$[nequa + 1]; glob_nequa=$[glob_nequa + 1]; }
	[ $ts -gt $ref_ts ] && { nwors=$[nwors + 1]; glob_nwors=$[glob_nwors + 1]; }
	[ $ts -lt $min_ts ] && { min_ts=$ts; }
    done
    avg_ts=`echo "$sum_ts / $REPS" | bc -l`
    std_ts=`echo "$sum_sq_ts / $REPS - $avg_ts * $avg_ts" | bc -l`
    avg_diff=`echo "$sum_diff / $REPS" | bc -l`
    std_diff=`echo "$sum_sq_diff / $REPS - $avg_diff * $avg_diff" | bc -l`
    fbest=`echo "$nbest / $REPS" | bc -l`
    fequa=`echo "$nequa / $REPS" | bc -l`
    fwors=`echo "$nwors / $REPS" | bc -l`
    printf "%s %d %d %g %g %g %g %g %g %g\n" $bf $ref_ts $min_ts $avg_ts $std_ts $avg_diff $std_diff $fbest $fequa $fwors
done
fbest=`echo "$glob_nbest / ($REPS * ${#FILES[@]})" | bc -l`
fequa=`echo "$glob_nequa / ($REPS * ${#FILES[@]})" | bc -l`
fwors=`echo "$glob_nwors / ($REPS * ${#FILES[@]})" | bc -l`
avg_diff=`echo "$glob_sum_diff / ($REPS * ${#FILES[@]})" | bc -l`
std_diff=`echo "$glob_sum_sq_diff / ($REPS * ${#FILES[@]}) - $avg_diff * $avg_diff" | bc -l`
printf "GLOBAL RESULTS: %g %g %g %g %g\n" $avg_diff $std_diff $fbest $fequa $fwors
exit 0