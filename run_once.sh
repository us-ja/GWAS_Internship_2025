n=300


start=6
method='sequential'
comment='test'
if [[ "$method" == "$isseed" ]]; then 
    value=$seed
else
    value=$start
fi
mkdir -p $method$comment$value
python3 convertold.py $n $method $start $comment
../espresso-logic-master/bin/espresso $method$comment$value/output_$n.txt >$method$comment$value/analysis_$n.txt 
python3 espresso_to_snp.py $n $method $value $comment
rm $method$comment$value/analysis_$n.txt
rm $method$comment$value/output_$n.log
rm $method$comment$value/output_$n.txt