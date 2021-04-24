# set the root folder; this might work as well
ROOT=/cs/natlang-expts/transitive_nmt #/local-scratch/nishant/fair/fairmod2

# paths to src_dictionary, checkpoint, and sentencepiece.model
DICTPATH=$ROOT/data-bin/faker/4/bpe/  # point to bpe folder
CKPTPATH=$ROOT/checkpoints/multi_fake_4
BPEMODEL=$ROOT/data-bin/faker/4/bpe/sentencepiece.bpe.model  # should match $DICTPATH/sentencepiece.bpe.model

# input and output directories for custom files
INPUT=""
OUTPUT=""

# also accepts the args --input_dir and --output_dir
python encoder_outs.py --dict $DICTPATH --checkpoint $CKPTPATH --spm $BPEMODEL

# naming of the checkpoints
# multi_fake = F0 (not required for analysis)
# multi_fake_[1-4] = Series F[1-4]
# random_fake_[1-4] = Random F[1-4]
# random_case_[1-4] = Cased F[1-4]

# naming of the data folders
# everything is inside `faker`. 
# goto `bpe` inside every folder
# 1,2,3,4 = Series F[1-4]
# randomF[1-4] = Random F[1-4]
# randomcase[1-4] = Cased F[1-4]