for i in {0..10000}; do
     file_name="${i}_*_blast_summary.csv"
        [ ! -f $file_name ] && echo "$file_name"
done
