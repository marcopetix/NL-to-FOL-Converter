import entity as Entity

def ent_recognition(doc):
    print("NAMED ENTITIES\n")
    for ent in doc.ents:
        print(ent.label_ + "(" + ent.text + ")")
