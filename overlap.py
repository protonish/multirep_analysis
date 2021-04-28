import argparse
import os
from collections import Counter, defaultdict
import itertools

parser = argparse.ArgumentParser("extract encoder outputs from a transformer model.")
parser.add_argument(
    "--input_dir",
    default="/local-scratch/nishant/fair/fairmod2/data-bin/faker/randomcase5/tok",
    help="directory containing tokenized data",
)
parser.add_argument(
    "--output_dir",
    default="results/",
    help="path to output directory.",
)
parser.add_argument(
    "--langs",
    nargs="+",
    default=["de", "a", "b"],
    help="langs to analyze.",
)
parser.add_argument(
    "--filenames",
    nargs="+",
    default=[
        "train.bpe.de-en.de",
        "train.bpe.a-en.a",
        "train.bpe.b-en.b",
        "train.bpe.c-en.c",
        "train.bpe.d-en.d",
        "train.bpe.e-en.e",
    ],
    help="filenames in the input_dir.",
)

parser.add_argument(
    "--checkpoint",
    default="/local-scratch/nishant/fair/fairmod2/checkpoints/multi_fake_4",
    help="path to saved model checkpoint (path only).",
)
parser.add_argument(
    "--spm",
    default="/local-scratch/nishant/fair/fairmod2/data-bin/faker/4/bpe/sentencepiece.bpe.model",
    help="path to sentencepiece model.",
)
args = parser.parse_args()


def get_token_vocab(text):
    subwords = Counter()
    for line in text:
        subwords.update(line.split(" "))
    return list(subwords.keys())


def read_text(input_dir, filename):
    with open(os.path.join(input_dir, filename)) as f:
        text = f.readlines()
    return text


def index_filenames(filenames):
    names = defaultdict(str)
    for filename in filenames:
        names[filename.split(".")[-1].strip()] = filename
    return names


def get_all_vocabs(input_dir, filenames, langs):
    vocab = {}
    for lang in langs:
        text = read_text(input_dir, filenames[lang])
        # print("{} -- {}".format(str(lang), str(filename.split(".")[-1])))
        print("Extracting vocab for lang {}.".format(lang))
        vocab[lang] = get_token_vocab(text)
    return vocab


def jaccard(lang1, lang2):
    intersection = len(list(set(lang1).intersection(lang2)))
    union = (len(lang1) + len(lang2)) - intersection
    return float(intersection) / union


def set_overlap(lang1, lang2):
    intersection = len(list(set(lang1).intersection(lang2)))
    # union = (len(lang1) + len(lang2)) - intersection
    return float(intersection) / min(len(lang1), len(lang2))


if __name__ == "__main__":
    fnames = index_filenames(args.filenames)
    vocab = get_all_vocabs(args.input_dir, fnames, args.langs)
    for key in vocab.keys():
        print(len(vocab[key]))
    for pair in list(itertools.combinations(vocab.keys(), 2)):
        if "de" in pair:
            print(
                "{} - {:.4f} - {:.4f}".format(
                    pair,
                    jaccard(vocab[pair[0]], vocab[pair[1]]),
                    set_overlap(vocab[pair[0]], vocab[pair[1]]),
                )
            )
