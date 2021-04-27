from fairseq.models.transformer import TransformerModel
import argparse
import os


parser = argparse.ArgumentParser("extract encoder outputs from a transformer model.")
parser.add_argument(
    "--input_dir",
    default="../data/semeval/tokenized/",
    help="directory containing tokenized data",
)
parser.add_argument(
    "--output_dir",
    default="results/",
    help="path to output directory.",
)
parser.add_argument(
    "--dict",
    default="/local-scratch/nishant/fair/fairmod2/data-bin/faker/4/bpe/",
    help="path to src dict.",
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


if __name__ == "__main__":
    """
    encoder.forward() returns a dict with the following keys:
    dict:
        - **encoder_out** (Tensor): the last encoder layer's output of
            shape `(src_len, batch, embed_dim)`
        - **encoder_padding_mask** (ByteTensor): the positions of
            padding elements of shape `(batch, src_len)`
        - **encoder_embedding** (Tensor): the (scaled) embedding lookup
            of shape `(batch, src_len, embed_dim)`
        - **encoder_states** (List[Tensor]): all intermediate
            hidden states of shape `(src_len, batch, embed_dim)` in order.
            Only populated if *return_all_hiddens* is True.
    """

    faker = TransformerModel.from_pretrained(
        args.checkpoint,
        checkpoint_file="checkpoint_best.pt",
        data_name_or_path=args.dict,
        bpe="sentecepiece",
        sentencepiece_model=args.spm,
    )

    # read input file to form a list of sentences using args.input_dir
    # this is a crude example
    sents = [
        "<en> Sie wächst im Winter und schrumpft im Sommer.",
        "<en> Sie wächst im Sommer und schrumpft im Winter.",
    ]
    sent_tok = [faker.encode(sent) for sent in sents]

    # we can use the model for translations; dont tokenize for translation;
    # model tokenizes input before translating.
    # uncomment the following lines
    print(faker.translate(sents))

    # separating the encoder module from pretrained model
    encoder = faker.models[0].encoder

    # batching sentences for a forward pass through the encoder
    batchwise_enc_out = []
    for batch in faker._build_batches(sent_tok, False):

        out = encoder.forward(batch["net_input"]["src_tokens"], return_all_hiddens=True)
        batchwise_enc_out.append(out["encoder_states"])

        # use batchwsie_enc_out or embeddings as you like and write file to args.output_dir
        print("\nenc_out shape is of (src_len, batch, embed_dim)")
        for batch_out in batchwise_enc_out:
            for layer, enc_out in enumerate(batch_out):
                print("Layer {} - {}".format(layer + 1, enc_out.shape))

        print("\nwe can also compute embeddings for input tokens")
        embeds_with_pos, embeds = encoder.forward_embedding(
            batch["net_input"]["src_tokens"]
        )
        print(
            "Embidding of shape (batch, src_len, embed_dim) : {}".format(embeds.shape)
        )
