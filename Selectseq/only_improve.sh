source ../venv/bin/activate
sel_file=sel
value=0
txt=.txt
intermediate="intermediate"
# start=6
# seed=18
initial=64

m=9

total_snp=$(awk -F'\t' 'NR==1{print NF}' HapMap.ped)
overcount=$((-6))
total_snp=`expr $total_snp + $overcount`
method='preselected'
int_size=$initial  
sel_size=$initial
new=$initial 
comment="improve"

seq 0 $sel_size | xargs -n1  > $sel_file$value$txt
cat $sel_file$value$txt > $intermediate$value$txt

   
int_size=`expr $int_size + 1` #add one size for element zero



mkdir -p $method$comment$value

echo "#this is not an actual result or log!! \n 0">$method$comment$value/result$sel_size.txt
b=0

while [ $new -lt $total_snp ]
do 
    python3 convert3.py $intermediate$value$txt $method $value $comment
    # echo $int_size "open int size $method$comment$value/analysis_$int_size.txt"
    ../../espresso-logic-master/bin/espresso $method$comment$value/output_$int_size.txt >$method$comment$value/analysis_$int_size.txt 
    python3 espresso_to_snp.py $int_size $method $value $comment
    rm $method$comment$value/analysis_$int_size.txt
    rm $method$comment$value/output_$int_size.log
    rm $method$comment$value/output_$int_size.txt
    
    
    sel_res=$(tail -1 $method$comment$value/result$sel_size.txt)

    int_res=$(tail -1 $method$comment$value/result$int_size.txt)
    
    # echo $int_res $sel_res
    
    
    # if  [ "$prev_res" -eq "$b" ] || [ "$curr_res" -lt "$prev_res" ];then
    #     echo "it works"
    # fi
    if  [ "$sel_res" -eq "$b" ] || [ "$int_res" -lt "$sel_res" ]        #first condition could also be written as [ "$initial" -eq "$new" ]
    then            #new gets accepted, initial should be accepted by default
        cat $intermediate$value$txt > $sel_file$value$txt
        sel_size=$int_size
        echo "Completed" $method$value "at" $(date '+%B %V %T:') "with accepted new=" $new
    else        #new gets rejected
        # echo "$new skipped"
        cat $sel_file$value$txt > $intermediate$value$txt
        int_size=$sel_size
    fi 
    int_size=`expr $int_size + 1`            #add 1 to count and add this to intermediate
    new=`expr $new + 1`                     #increase new always and add this
    echo $new >> $intermediate$value$txt
done
python3 convert3.py $intermediate$value$txt $method $value $comment
../../espresso-logic-master/bin/espresso $method$comment$value/output_$int_size.txt >$method$comment$value/analysis_$int_size.txt 
python3 espresso_to_snp.py $int_size $method $value $comment
rm $method$comment$value/analysis_$int_size.txt
rm $method$comment$value/output_$int_size.log
rm $method$comment$value/output_$int_size.txt


sel_res=$(tail -1 $method$comment$value/result$sel_size.txt)
int_res=$(tail -1 $method$comment$value/result$int_size.txt)
if  [ "$sel_res" -eq "$b" ] || [ "$int_res" -lt "$sel_res" ]        #first condition could also be written as [ "$initial" -eq "$new" ]
then            #new gets accepted, initial should be accepted by default
    cat $intermediate$value$txt > $sel_file$value$txt
    sel_size=$int_size
    echo "Completed" $method$value "at" $(date '+%B %V %T:') "with accepted new=" $new
else        #new gets rejected
    # echo "$new skipped"
    rm $method$comment$value/result$int_size.txt 
fi 
rm $intermediate$value$txt
rm $method$comment$value/result$initial.txt
final=$(tail -1 $method$comment$value/result$sel_size.txt)
echo "Finished "$method$comment$value " at " $(date '+%B %V %T:') "now with only $final elements"
echo $sel_size



