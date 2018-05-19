# coding=iso-8859-1
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import defaultdict
import re
import os
import io


data_path = os.path.join(".", "text")

aa = os.path.join(data_path, "AA")
ab = os.path.join(data_path, "AB")
ac = os.path.join(data_path, "AC")
ad = os.path.join(data_path, "AD")


def get_msgdir(path):
    filelist = os.listdir(path)
    filelist = filter(lambda x: x != 'cmds', filelist)
    all_msgs = [get_msg(os.path.join(path, f)) for f in filelist]
    result = ""
    for msg in all_msgs:
        result += msg
    return result

def get_msg(path):
    with open(path, 'rU') as con:
        msg = con.readlines()
        return ''.join(msg)


re_apostroph = re.compile("\"")

def re_title_cleaned(matchobj):
    return matchobj.group(1) + re_apostroph.sub("", matchobj.group(2)) + matchobj.group(3)


def get_msg_clean(message):
    msg = re.sub('<ns>.*?</ns>','', message)
    msg = re.sub('<id>.*?</id>','', msg)
    msg = re.sub('<parentid>.*?</parentid>','', msg)
    msg = re.sub('<timestamp>.*?</timestamp>','', msg)
    msg = re.sub('<username>.*?</username>','', msg)
    msg = re.sub('<contributor>.*?</contributor>','', msg)
    msg = re.sub('<comment>.*?</comment>','', msg)
    msg = re.sub('<model>.*?</model>','', msg)
    msg = re.sub('<format>.*?</format>','', msg)
    msg = re.sub('\((.*?)\)', '', msg)
    msg = re.sub('! style="background-color: #b0c4de"', '', msg)

    re_title = re.compile("(title=\")(.*)(\">)")
    re_xml_tag = re.compile("<[^<]+>")
    re_and = re.compile("&")
    re_lower = re.compile("< ")
    re_brackets = re.compile('[\[\]{}()<>]')
    re_slash = re.compile(r"^\|(?:\\.|[^\|\\])*\|")

    msg = re.sub("_+\w+", '', msg)
    msg = re.sub("\|+", '', msg)
    msg = re.sub('align="center" colspan="2"', '', msg)
    msg = re.sub('width="300" style="padding:0px;"', '', msg)
    msg = re_title.sub(re_title_cleaned, msg)
    msg = re_xml_tag.sub("", msg)
    msg = re_and.sub("&amp;", msg)
    msg = re_lower.sub("&lt; ", msg)
    msg = re_brackets.sub("", msg)
    msg = re_slash.sub("", msg)

    msg = msg.replace('This vegetable related article is a . You can Wikipedia by  expanding it', '')
    msg = msg.replace('\".', '')
    msg = msg.replace('\"', '')
    msg = re.sub("\n\s*\n*", "\n", msg)

    return msg


a = get_msg_clean(get_msgdir(aa))
b = get_msg_clean(get_msgdir(ab))
c = get_msg_clean(get_msgdir(ac))
d = get_msg_clean(get_msgdir(ad))

def ngrams_count(words):
    word_dict = defaultdict(lambda: 0)
    for word in words:
        word_dict[word.strip()] += 1
    return word_dict


# all wikipedia text

total = a + b + c + d

# generate unigrams

# words = word_tokenize(total.decode("utf-8"))
# words_dict = ngrams_count(words)
#
# for key in words_dict.keys():
#     if len(key) == 1 or key.isdigit():
#         del words_dict[key]
#
# with io.open("unigram.txt", 'w', encoding='utf-8') as f:
#     f.writelines(key + " " + str(value) + u'\n' for key, value in sorted(words_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True))
#     f.close()


# generate bigrams

bigram_array = []
sent_tokenize_list = sent_tokenize(total.decode("utf-8"))
for sent in sent_tokenize_list:
    for ngram in ngrams(sent.split(' '), 2):
        bigram_array.append(' '.join(i for i in ngram))

bigrams_dict = ngrams_count(bigram_array)

with io.open("bigram.txt", 'w', encoding='utf-8') as f:
    f.writelines(key + " " + str(value) + u'\n' for key, value in sorted(bigrams_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True))
    f.close()


# generate trigrams

# trigram_array = []
# for sent in sent_tokenize_list:
#     for ngram in ngrams(sent.split(' '), 3):
#         trigram_array.append(' '.join(i for i in ngram))
#
# trigram_dict = ngrams_count(trigram_array)
#
# with io.open("trigram.txt", 'w', encoding='utf-8') as f:
#     f.writelines(key + " " + str(value) + u'\n' for key, value in sorted(trigram_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True))
#     f.close()
