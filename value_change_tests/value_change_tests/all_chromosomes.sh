method='sequential'
source ../venv/bin/activate
for start in 87726 177524 252386 318515 387532 459285 518389 577032 627364 684589 739873 792438 832928 868072 900080 933899 963017 994672 1014334 1042282 1057764
do
    seed=8
    n=80
    comment='chr'
    isseed='seeded'
    if [[ "$method" == "$isseed" ]]; then 
        value=$seed
    else
        value=$start
    fi



    
    echo "Started with seed" $method$comment$value "at" $(date '+%B %V %T:')
    mkdir -p $method$comment$value
    while [ $n -lt 901 ]
    do 
        python3 trick.py $n $method $value $comment
        ../../espresso-logic-master/bin/espresso $method$comment$value/output_$n.txt >$method$comment$value/analysis_$n.txt 
        python3 espresso_to_snp.py $n $method $value $comment
        rm $method$comment$value/analysis_$n.txt
        rm $method$comment$value/output_$n.log
        rm $method$comment$value/output_$n.txt
        echo "Completed" $method$value "at" $(date '+%B %V %T:') "with n="$n
        n=`expr $n + 5`
    done 

    echo "Finished "$method$comment$value " at " $(date '+%B %V %T:')
done