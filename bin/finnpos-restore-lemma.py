#! /usr/bin/env python3

from sys import stdin, stdout, stderr, argv
from difflib import get_close_matches
from re import sub

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
        # if (omorfiOrig == '[]'):
            # print ("Bla", omorfiOrig)
            # continue
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
        

        sourceFinnPos = '[SOURCE=FINNPOS][WORD_ID='+ lemma.replace(HASH,"#") +']'+ label.replace("|",'')
        # print(sourceFinnPos)
        # print('%s\t%s\t%s\t%s\t%s' % (wf, feats, lemma.replace(HASH,"#"), label, ann), file=stderr)
        

        origOmorfiList = ['[SOURCE=OMORFI]' + x for x in (omorfiOrig.replace("['",'').replace("']",'').replace("]', '[WORD_ID=", ']\t[WORD_ID=')).split('\t')]
        # print (origOmorfiList, file=stderr)
        
        if (len(origOmorfiList) == 1):
            if (origOmorfiList[0] == '[SOURCE=OMORFI][]'):
                print (sourceFinnPos)
                continue
            print (origOmorfiList[0])

        if (len(origOmorfiList) > 1):
            
            # Filter only those omorfi results that have matching lemma with finnpos
            matchingOmorfi = []
            for line in origOmorfiList:
                cleanLine = sub(r"_\d", "", line)
                # print("Line: ", cleanLine)
                if ('[WORD_ID='+lemma.replace(HASH,"#")+']') in cleanLine:
                    matchingOmorfi.append(line)
                    
            if (len(matchingOmorfi) == 1 ):
                print ('%s' % matchingOmorfi[0].strip())
                continue
                
            # print ("matchingOmorfi", matchingOmorfi)
            # print('[WORD_ID='+lemma.replace(HASH,"#")+']'+ label.replace("]|[","]["))
            
            # Choose just one
            oneOmorfi = get_close_matches('[WORD_ID='+lemma.replace(HASH,"#")+']'+ label.replace("]|[","][") , matchingOmorfi, 1)
 
            # if there is one match
            if (len(oneOmorfi) == 1):
                # print ('%s' % oneOmorfi[0].strip().replace("['",'').replace("]'","]").replace("'[",'['))
                print ('%s' % oneOmorfi[0].strip())
            elif(len(oneOmorfi) == 0 and len(matchingOmorfi) > 1):
                print ('%s' % matchingOmorfi[0].strip())
            else:
                print (origOmorfiList[0])

