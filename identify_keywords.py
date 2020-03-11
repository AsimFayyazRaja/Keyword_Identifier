from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk import everygrams
from nltk.corpus import stopwords
import copy
import warnings
warnings.filterwarnings("ignore")

cachedStopWords = stopwords.words("english")

def exists(gram,keyword):
    "checks if an n-gram  already exists in the keywords or not"
    keyword=keyword.lower()
    
    #makes 5 n-grams of the keyword to match with the given keyword
    keyword=list(everygrams(keyword.split(), 1, 5))
    new_keyword=[]
    
    for p in keyword:
        p=" ".join(p)
        new_keyword.append(p)
    keyword=new_keyword
    if gram.lower() in keyword:
        return True
    else:
        return False

def remove_stopwords(text):
    "Filters out the stopwords from the sentence to avoid false positives"
    text = ' '.join([word for word in text.split() if word not in cachedStopWords])
    return text


def is_same(word1,word2):
    "Tells if two words are same but with different spaces and case of letters"
    word1=word1.replace(" ","")
    word2=word2.replace(" ","")
    
    if word1.lower()==word2.lower():
        return True
    else:
        return False


def already_exists(ngram,keywords,partial_match,sp_char=' '):
    "Tells about an n-gram is already present in the list of projects found or not"
    for pr in keywords:
        pr1=[]
        pr=pr.split(sp_char)
        for val in pr:
            pr1.append(val.lower())
        if ngram.lower() in pr1 and ngram.lower() not in partial_match:
            return True
    return False

def find_sub_keywords(all_keywords,grams,keys_found,sent,grams_done,partial_match,keywords_indices,splitting_char):
    #handling 1grams separately because they are sort of wildcards
    count=0
    
    one_word_projs=[]
    try:
        msg=sent.split()
    except:
        msg=sent
    #print("splitting char: ", splitting_char)
    for m in msg:
        for j,proj in enumerate(all_keywords):
            proj1=proj.split(splitting_char)
            #print(proj1)
            for p in proj1:
                ratio=fuzz.ratio(m.lower(),p.lower())
                if ratio>=85:   # if ratio is more than 85 then return keyword with fuzzy matching
                    if (proj not in keys_found) and (already_exists(m,grams_done,partial_match,splitting_char)==False):
                        
                        keys_found.append(proj)
                        keywords_indices.append(j)
                        one_word_projs.append(proj)
                        count+=1
    
    return keys_found,keywords_indices
    
def find_projs(all_keywords,grams,sent,prjs,split_char=' '):
    grams_done=[]  #grams that are found
    from fuzzywuzzy import fuzz  # do fuzzy matching here to extract words that are not detected by NER        
    keys_found=[]
    keywords_indices=[]
    partial_match=[]
    for gram in grams:
        gram1=split_char.join(gram)
        for i,proj in enumerate(all_keywords):
            ratio=fuzz.ratio(gram1.lower(),proj.lower())
            # if ratio is greater than 80 and gram is not already added
            if ratio>80 and already_exists(gram1,keys_found,partial_match,split_char)==False and proj not in keys_found:
                if is_same(gram1,proj):   # if gram is found in the keyword
                    keys_found.append(proj)
                    keywords_indices.append(i)
                    grams_done.append(gram1)
                    
            if (already_exists(gram1,keys_found,partial_match,split_char)==False) and (proj not in keys_found) and (exists(gram1,proj)):
                partial_match.append(gram1.lower())   # add partial match if no exact match found
                keys_found.append(proj)
                keywords_indices.append(i)
                grams_done.append(gram1)
    
    try:   # find keyowrds, separated with space 
        p1,p1ind=find_sub_keywords(all_keywords,grams,keys_found,sent,grams_done,partial_match,keywords_indices,' ')
        p1=set(p1)
        p1ind=set(p1ind)
        
    except Exception as e:
        
        p1=set()
        pass    
    try:         # find keyowrds, separated with hyphen
        p2,p2ind=find_sub_keywords(all_keywords,grams,projs_found,sent,grams_done,partial_match,keywords_indices,'-')
        p2=set(p2)
        p2ind=set(p2ind)
        
    except Exception as e:
        p2=set()
        pass
    
    try:     # find keyowrds, separated with underscore
        p3,p3ind=find_sub_keywords(all_keywords,grams,keys_found,sent,partial_match,keywords_indices,grams_done,'_')
        p3=set(p3)
        p3ind=set(p3ind)
        
    except Exception as e:
        p3=set()
        pass
    p1=p1.union(p2)
    p1=p1.union(p3)
    
    p2=list(p2)
    
    #removing additional projects if an exact match is found
    all_keywords1=list(p1)
    all_keywords2=[]
    for p in all_keywords1:
        p=p.lower()
        all_keywords2.append(p)
    
    
    
    
    all_keywords0=[]
    for p in all_keywords:
        p=p.lower()
        all_keywords0.append(p)
    all_keywords=all_keywords0
    
    for g in grams:     # finding exact match with an n-gram
        g=list(g)
        try:
            if '' in g:
                g.remove('')
                
            elif ' ' in g:
                g.remove(' ')
                
        except:
            pass
        
        if len(g)>1:
            g=" ".join(g)
            
            try:   # get partial and exact match from all projects here
                partial=[]
                for i,ap in enumerate(all_keywords):
                    if g.strip() in ap:
                        partial.append(prjs[i])
                try:
                    r=all_keywords.index(g.strip())
                    
                except Exception as e:
                    r=-1
                    pass
                if r!=-1:
                    return set([prjs[r]])
                if partial != []:
                    return partial
                
            except Exception as e:
                pass
        else:
            g=" ".join(g)
            if g== " " or g == "":
                continue
            
            try:   # get partial and exact match from all projects here
                partial=[]
                for i,ap in enumerate(all_keywords):
                    if " "+g+" " in ap:
                        partial.append(prjs[i])
                        
                    else:
                        try:
                            if ap.split().index(g)==len(ap.split())-1 or ap.split().index(g)==0:
                                partial.append(prjs[i])
                        except:
                            pass
                try:
                    r=all_keywords.index(g.strip())
                    
                    #print("R: ", r)
                except Exception as e:
                    r=-1
                    pass
                if r!=-1:
                    return set([prjs[r]])
                if partial != []:
                    return partial
                
            except Exception as e:
                #print(e)
                pass
    p1ind=p1ind.union(p2ind)
    p1ind=p1ind.union(p3ind)
    p1ind=list(p1ind)
    
    
    p1_indices=[]
    p1=list(p1)
    for i in p1ind:
        if type(i) is int:
            p1_indices.append(i)
    prjs=np.array(prjs)
    p1=prjs[p1_indices]
    return set(p1)


def identify_keywords(all_keywords,sent,split_char=' '):
    "Identifies keywords present in sentence"
    all_keywords1=[]
    
    prjs=copy.deepcopy(all_keywords)
    
    for p in all_keywords:
        p=p.replace("_"," ")
        p=p.replace("-"," ")
        p=p.replace(": "," ")
        p=p.replace(":"," ")
        
        
        all_keywords1.append(p)
    all_keywords=all_keywords1
    
    sent1=[]
    #clean the sentence for different punctuations
    for s in sent.split():
        s=s.replace("_"," ")
        s=s.replace("-"," ")
        s=s.replace(": "," ")
        s=s.replace(":"," ")
        sent1.append(s+" ")
        
    sent=''.join(sent1)
    sent=sent.lower()
    keys_found=[]
    #sent=remove_stopwords(sent)  #remove stopwords
    
    grams=list(everygrams(sent.split(split_char), 1, 5))  #make ngrams upto 5
    grams.reverse()  #reverse the string for not finding 1 gram which is already found in 2 grams etc
    try:
        p1=find_projs(all_keywords,grams,sent,prjs,split_char)
    except Exception as e:
        p1=[]
    return p1
