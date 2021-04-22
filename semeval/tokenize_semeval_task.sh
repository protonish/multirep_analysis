mono_dir=../data/semeval/original/test/subtask1-monolingual/data/
cross_dir=../data/semeval/original/test/subtask2-crosslingual/data/
args="--model ../data/bpe_model/sentencepiece.bpe.model --output_format id"

for f in $( ls $mono_dir |grep "^\(en\|de\)\." ); do
  python ../spm_encode.py \
    --inputs <( cat $mono_dir/$f |sed 's/	.*//g' ) \
    --outputs _tmp_left \
    $args > /dev/null 2>&1
  python ../spm_encode.py \
    --inputs <( cat $mono_dir/$f |sed 's/.*	//g' ) \
    --outputs _tmp_right \
    $args > /dev/null 2>&1
  paste _tmp_left _tmp_right > ../data/semeval/tokenized/$f
done
for f in $( ls $cross_dir |grep "^en-de\." ); do
  python ../spm_encode.py \
    --inputs <( cat $cross_dir/$f |sed 's/	.*//g' ) \
    --outputs _tmp_left \
    $args > /dev/null 2>&1
  python ../spm_encode.py \
    --inputs <( cat $cross_dir/$f |sed 's/.*	//g' ) \
    --outputs _tmp_right \
    $args > /dev/null 2>&1
  paste _tmp_left _tmp_right > ../data/semeval/tokenized/$f
done
rm _tmp_left _tmp_right
