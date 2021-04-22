import string
import random
from collections import Counter
import fire


class FakeLang:
    """
    Create fake langauge text based on substitution ciphers
    following syntax and vocab from a base source language text.
    """

    def __init__(self, destdir, srcdir, origde):
        self.destdir = destdir
        self.srcdir = srcdir
        self.origde = origde
        # real src file name
        self.realsrc = "train.de-en.de"
        # fake language names (abcd..xyzABCD..XYZ)
        # each char is the fake lang name
        self.fake_langs = string.ascii_letters

    def generate(
        self,
        PREF: str,
        key: int,
        keylist: [int],
        inrange: bool,
        trgtoken: bool = False,
        srctoken: bool = False,
    ):

        self.pref = PREF
        self.key = KEY = key
        self.range = RANGE = inrange

        with open(self.srcdir + self.origde, "r") as de:
            ode = de.readlines()

        # if srctoken:
        #     with open(self.destdir + self.realsrc, "w") as destde:
        #         for line in ode:
        #             destde.write("<de>" + " " + line)
        #     print("Finished writing file for lang {}".format("de"))
        # elif trgtoken:
        #     with open(self.destdir + self.realsrc, "w") as destde:
        #         for line in ode:
        #             destde.write("<en>" + " " + line)
        #     print("Finished writing file for lang {}".format("de"))

        # A list containing all characters from text
        char_vocab = self.get_char_vocab(ode, alphaonly=True)
        # shifted_vocab = self.shift_vocab(char_vocab, KEY)

        if KEY > 2 and RANGE and len(keylist) == 0:
            # generate train data for all KEYs in range 1-KEY
            # only works when KEY is greater than 1 and RANGE is true
            print("Generating files for langs in range (1-{})".format(KEY))
            for key in range(1, KEY):
                # cipher_text = []
                shifted_vocab = self.shift_vocab(char_vocab, key)
                with open(
                    self.destdir
                    + PREF
                    + self.fake_langs[key - 1]
                    + "-en."
                    + self.fake_langs[key - 1],
                    "w",
                ) as f:
                    for line in ode:
                        cline = self.monophonic(line, char_vocab, shifted_vocab)
                        # cipher_text.append(cline)
                        if srctoken:
                            f.write("<{}> {}".format(self.fake_langs[key - 1], cline))
                        elif trgtoken:
                            f.write("<en> {}".format(cline))
                        else:
                            f.write(cline)

                print(
                    "Finished writing file for lang {}".format(self.fake_langs[key - 1])
                )

        elif len(keylist) > 0:
            # generate train data for all KEYs in the KEYLIST
            # ignores KEY and RANGE
            # NOTE: unlike the generate-in-range paradigm above, we name the
            # fake-langs in the range (aa, bb, ..) incrementally
            print(
                "Generating {} files for langs in the keylist {}".format(
                    len(keylist), keylist
                )
            )
            for i, key in enumerate(keylist):
                shifted_vocab = self.shift_vocab(char_vocab, key)
                with open(
                    self.destdir
                    + PREF
                    + self.fake_langs[i]
                    + "-en."
                    + self.fake_langs[i],
                    "w",
                ) as f:
                    for line in ode:
                        cline = self.monophonic(line, char_vocab, shifted_vocab)
                        # cipher_text.append(cline)
                        if srctoken:
                            f.write("<{}> {}".format(self.fake_langs[i], cline))
                        elif trgtoken:
                            f.write("<en> {}".format(cline))
                        else:
                            f.write(cline)

                print("Finished writing file for lang {}".format(self.fake_langs[i]))

        else:
            print("Generating files for one lang ({})".format(KEY))
            cipher_text = []
            shifted_vocab = self.shift_vocab(char_vocab, KEY)
            with open(
                self.destdir
                + PREF
                + self.fake_langs[KEY - 1]
                + "-en."
                + self.fake_langs[KEY - 1],
                "w",
            ) as f:
                for line in ode:
                    cline = self.monophonic(line, char_vocab, shifted_vocab)
                    # cipher_text.append(cline)
                    if srctoken:
                        f.write("<{}> {}".format(self.fake_langs[KEY - 1], cline))
                    elif trgtoken:
                        f.write("<en> {}".format(cline))
                    else:
                        f.write(cline)

                print(
                    "Finished writing file for lang {}".format(self.fake_langs[KEY - 1])
                )

        # print(ode[4])
        # print(cipher_text[4:6])
        print("Done! Check the dir: {}".format(DESTDIR))

    def get_char_vocab(self, text, alphaonly=False):
        char_counter = Counter()
        for line in text:
            if alphaonly:
                char_counter.update(c for c in line if c.isalpha())
            else:
                char_counter.update(c for c in line)

        chars = sorted(char_counter.keys())
        return chars

    def shift_vocab(self, all_letters, key):
        d = {}
        for i in range(len(all_letters)):
            d[all_letters[i]] = all_letters[(i + key) % len(all_letters)]
        return d

    def monophonic(self, plain_txt: str, all_letters: list, holder: dict):
        cipher_txt = []
        for char in plain_txt:
            if char in all_letters:
                temp = holder[char]
                cipher_txt.append(temp)
            else:
                temp = char
                cipher_txt.append(temp)

        cipher_txt = "".join(cipher_txt)
        return cipher_txt

    def homophonic(self, plaintext, switchout):
        ret = ""
        for i in range(len(plaintext)):
            ret += (
                "%"
                if random.random() > switchout
                and (plaintext[i] in ["a", "e", "i", "o", "u"])
                else "-"
            )
        return ret

    def prependtok(
        self,
        pref: str = None,
        srctoken: bool = False,
        trgtoken: bool = True,
        filename: str = None,
        token: str = None,
        override=False,
    ):
        if filename is not None:
            with open(self.destdir + filename, "r") as de:
                ode = de.readlines()
                pref = filename
        else:
            assert pref is not None, "One of pref and filename must be provided"
            with open(self.srcdir + pref, "r") as de:
                ode = de.readlines()
        # crude way to check if ta ag already exists
        tagcount = 0
        for i in range(5):
            if "<" and ">" in ode[i][:4]:
                tagcount += 1
        existingtag = ode[0][:4]

        pref = pref.replace("0", "")
        if token is not None:
            if tagcount == 5 and override:
                print(
                    "Existing tag {} found. Overriding with <{}>".format(
                        existingtag, token
                    )
                )
                with open(self.destdir + "tag." + pref, "w") as destde:
                    for line in ode:
                        destde.write("<{}> {}".format(token, line[5:]))
                print(
                    "Finished prepending {} file with {}\nCheck filename {}".format(
                        pref, token, "tag." + pref
                    )
                )
            else:
                print(
                    "A tag **might** be existing, not sure. Just prepending <{}>".format(
                        token
                    )
                )
                with open(self.destdir + "tag." + pref, "w") as destde:
                    for line in ode:
                        destde.write("<{}> {}".format(token, line))
                print(
                    "Finished prepending {} file with {}\nCheck filename {}".format(
                        pref, token, "tag." + pref
                    )
                )
        else:
            if srctoken:
                with open(self.destdir + pref, "w") as destde:
                    for line in ode:
                        destde.write("<de>" + " " + line)
                print("Finished prepending {} file with srctoken".format(pref))
            elif trgtoken:
                with open(self.destdir + pref, "w") as destde:
                    for line in ode:
                        destde.write("<en>" + " " + line)
                print("Finished prepending {} file with trgtoken".format(pref))


def fetch(
    series=False,
    key=0,
    keylist: [int] = [],
    gen=False,
    prepend=False,
    trgtoken=False,
    token=None,
    split=None,
    filename=None,
    override=False,
):
    if gen:
        if len(keylist) == 0:
            assert key > 0, "Key must be greater than 0 when keylist is not provided."
        if len(keylist) > 0:
            assert key == 0, "Keylist must be null when Key is provided."
            for k in keylist:
                k = int(k)
                assert (
                    k > 0
                ), "Keys should start from 1. A key of 0 means 0 shift in vocab."
            assert len(keylist) == len(
                set(keylist)
            ), "Duplicate keys found! All keys in keylist should be unique."

    if split is not None:
        assert split in [
            "train",
            "valid",
            "test",
        ], "Prefix should be one of train/valid/test."
    if token is not None:
        assert prepend is True, "Prepend and token both should be supplied"
    if filename is not None:
        assert split is None, "When provising filename, split must be None (removed)"
    return (
        key,
        series,
        gen,
        prepend,
        trgtoken,
        split,
        token,
        filename,
        override,
        keylist,
    )


if __name__ == "__main__":
    """
    Step1:  Set SRCDIR and DSTDIR for reading and writing data.
    set ODET = the 'real' text file name -> [ODET is Orig De Text]
    These arguments create the faker instance from class.

    Step 2: faker.generate() generates data. Set a prefix (TRAINPREF). this will generate files named
    'prefix'.a-en.a , 'prefix'.b-en.b incrementally to match the no of keys

    usage to generate ciphers from a list of keys:
        python faker.py --key 0 --keylist [1,2,3,4,5] --gen --notrgtoken
    """
    # paths to files
    DATAROOT = "/local-scratch/nishant/fair/fairmod2/data-bin/"
    SRCDIR = DATAROOT + "iwslt17.real.de/"
    DESTDIR = DATAROOT + "faker/randomF4/"  # "fake/"
    ODET = "train.de-en.de"
    ODEV = "valid0.de-en.de"

    TRAINPREF = "train."
    VALIDPREF = "valid0."

    (
        key,
        inrange,
        gen,
        prepend,
        trgtoken,
        split,
        token,
        filename,
        override,
        keylist,
    ) = fire.Fire(
        fetch
    )  # pylint: disable=no-value-for-parameter

    faker = FakeLang(DESTDIR, SRCDIR, ODET)
    if gen:
        faker.generate(TRAINPREF, key, keylist, inrange, trgtoken)
    if prepend:
        if filename is not None:
            faker.prependtok(
                trgtoken=False, filename=filename, token=token, override=override
            )
        else:
            if split == "train":
                faker.prependtok(pref=ODET, srctoken=True, trgtoken=False)
            elif split == "valid":
                faker.prependtok(pref=ODEV, trgtoken=trgtoken)

        # else:
        #     faker.prependtok(pref=ODEV, trgtoken=trgtoken)

    # usage

    # python faker.py --key 3 --series/noseries --gen/nogen --prepend/noprepend --trgtoken/notrgtoken --split [train/valid/test]
