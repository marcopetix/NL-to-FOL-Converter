import spacy
import neuralcoref

nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)

def spacy_parsing(text):
    return nlp(text)

def spacy_parsing_coref(text):
    doc = nlp(text)
    print("{:<50}{:<150}".format("Sentence inserted by the user: ", doc.text))
    if doc._.has_coref:
        print("{:<50}{:<150}".format("Mentions clusters", str(doc._.coref_clusters)))
        new_doc = str(doc._.coref_resolved)
        print("{:<50}{:<150}".format("Sentence altered by Neuralcoref: ", new_doc))
        return nlp(new_doc)
    else:
        return doc

def spacy_parsing_coref_poss(text):
    doc = nlp(text)
    if doc._.has_coref:
        poss_clusters = []
        for x in doc._.coref_clusters:
            poss_mention = []
            i = 0
            for y in x.mentions:
                if y is not x.main:
                    token = doc[y.end - 1]
                    if token.dep_ is "poss":
                        poss_mention.append(i+1)
                i += 1
            poss_clusters.append([x.main.text, poss_mention])

        new_doc = str(doc._.coref_resolved)
        for cluster in poss_clusters:
            for occurence in cluster[1]:
                # Finding nth occurrence of substring
                val = -1
                for i in range(0, occurence):
                    val = new_doc.find(cluster[0], val + 1)
                # Printing nth occurrence ends at
                index = val + len(cluster[0])
                new_doc = new_doc[:index] + "'s" + new_doc[index:]
        return nlp(new_doc)
    else:
        return doc
