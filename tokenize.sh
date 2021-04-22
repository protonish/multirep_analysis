SP_MODEL=path/to/sentencepiece.bpe.model
DATA=path/to/data
OP=path/to/output/with/filename

echo "Encoding text with learned BPE..."
python spm_encode.py \
    --model "$SP_MODEL" \
    --output_format=piece \
    --inputs $DATA \
    --outputs $OP \
    --min-len 1 --max-len 250

echo "Done!"