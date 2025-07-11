source ../venv/bin/activate
method='seeded'

start=6
ending=".py"
for transformation in binrand trick
do
    for seed in 10 23 31 
    do 
        n=80
        comment=$transformation
        isseed='seeded'
        if test "$method" = "$isseed" ; then 
		value=$seed
		echo "here"
        else
            value=$start
        fi



        
        echo "Started with seed" $method$comment$value "at" $(date '+%B %V %T:')
        mkdir -p $method$comment$value
        while [ $n -lt 90 ]
        do 
            python3 $transformation$ending $n $method $value $comment
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
done
