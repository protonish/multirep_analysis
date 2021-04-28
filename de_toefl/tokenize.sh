echo Tokenizing with $1/sentencepiece.bpe.model

toefl_file=../data/analogy/de_toefl_subset.txt
args="--model ../data/bpe_model/$1/sentencepiece.bpe.model --output_format id"

for column in {1..6}; do
   python ../spm_encode.py \
    --inputs <( cat $toefl_file |tail -n+2 |sed 's/^/<de> /g' |awk "{print \$${column}}" ) \
    --outputs _c$column \
    $args > /dev/null 2>&1
done
paste _c{1..6} > de_toefl_tokenized.txt
rm _c{1..6}
