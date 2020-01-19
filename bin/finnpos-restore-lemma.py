#! /usr/bin/env python3

from sys import stdin, stdout, stderr, argv
from difflib import get_close_matches

HASH="<HASH>"
all_lemmas = 0

def part_count(lemma):
    return lemma.count('#')

def compile_dict(label_lemma_pairs):
    res = {}

    for label, lemma in label_lemma_pairs:
        if label in res:
            old_lemma = res[label]
            if old_lemma != lemma:
                if part_count(old_lemma) > part_count(lemma):
                    res[label] = lemma
                elif all_lemmas and part_count(old_lemma) == part_count(lemma):
                    res[label] = "%s|%s" % (old_lemma.replace("#",HASH),lemma)
        else:
            res[label] = lemma

    return res

if "--all-lemmas" in argv:
    all_lemmas = 1
elif len(argv) > 1:
    stderr.write("ERROR: Argument %s unknown.\n" % argv[1])
    exit(1)

for line in stdin:
    line = line.strip()

    if line == '':
        print('')
        stdout.flush()
    else:
        wf, feats, lemma, label, ann, omorfiOrig = line.split('\t')
        # print (wf)
        if (omorfiOrig == '[]'):
            print (omorfiOrig)
            continue
        # print(ann)
        lemmas = ann
        if ann.find(' ') != -1:
            lemmas = ann[:ann.find(' ')]
            ann = ann[ann.find(' ') + 1:]
        else:
            ann = '_'
        
        lemma_dict = {}
        if lemmas != '_':
            lemma_dict = compile_dict(eval(lemmas))
        
        if label in lemma_dict:
            lemma = lemma_dict[label]
            lemma = lemma.lower()
            lemma = lemma.replace('#','')
        
        
        origOmorfiList = (omorfiOrig.replace("['",'').replace("']",'').replace("]', '[WORD_ID=", ']\t[WORD_ID=')).split('\t')
        
        if (len(origOmorfiList) == 1):
            print (origOmorfiList[0])

        if (len(origOmorfiList) > 1):
            
            # Filter only those omorfi results that have matching lemma with finnpos
            matchingOmorfi = []
            for line in origOmorfiList:
                if ('[WORD_ID='+lemma.replace(HASH,"#")+']') in line:
                    matchingOmorfi.append(line)
               

            # Choose just one
            oneOmorfi = get_close_matches('[WORD_ID='+lemma.replace(HASH,"#")+']'+ label.replace("]|[","][") , matchingOmorfi, 1)

            # if there is one match
            if (len(oneOmorfi) == 1):
                # print ('%s' % oneOmorfi[0].strip().replace("['",'').replace("]'","]").replace("'[",'['))
                print ('%s' % oneOmorfi[0].strip())
            else:
                # one from the original
                # print (origOmorfiList[0].replace("['",'').replace("']",''))
                print (origOmorfiList[0])

