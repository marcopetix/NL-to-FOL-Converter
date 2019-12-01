import library
import predicate as Predicate
import variable as Variable

dep_modifiers = library.dep_modifiers

def dep_acl(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if not library.add_to_subj_list(target_token, token, variables, predicates, num_of_terms):
        library.make_predicate(predicates, token, token, target_token)

def dep_advmod(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if not library.get_predicate(token, predicates):
        if token.tag_ == "WRB":
            cond_tokens.append(token)
            library.make_predicate(predicates, token, token.head)
        else:
            dep_modifier(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens)

def dep_auxpass(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token not in passive_tokens:
        passive_tokens.append(target_token)

def dep_modifier(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if not library.get_predicate(token, predicates):
        target_token = token.head
        if target_token.dep_ in dep_modifiers:
            while target_token.dep_ in dep_modifiers:
                target_token = target_token.head
        elif target_token.dep_ is "xcomp":
            target_token = library.until_not("xcomp", target_token)
        library.make_mono_predicate(target_token, predicates)
        library.make_predicate(predicates, token, target_token)

def dep_ccomp(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    library.make_mono_predicate(token, predicates)
    if not library.add_to_obj_list(token, target_token, variables, predicates, num_of_terms):
        library.make_predicate(predicates, target_token, target_token, None, token)

def dep_compound(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token.dep_ is "poss":
        library.make_predicate(predicates, token, target_token)
    elif target_token.dep_ is "conj":
        conj_head = library.until_not("conj", token.head)
        if conj_head.dep_ in dep_modifiers:
            conj_head_predicate = library.get_predicate(conj_head, predicates)
            library.make_predicate(predicates, token.head, conj_head_predicate.dep_token, None, None,token)
    else:
        dep_modifier(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens)

def dep_conj(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    token_predicate = library.get_predicate(token, predicates)
    target_predicate = library.get_predicate(target_token, predicates)
    conj_head = library.until_not("conj", token)
    if conj_head.dep_ == "ROOT" or conj_head.dep_ is "relcl" or conj_head.dep_ is "advcl": #NON PUò CONSIDERARE I CASI COME "TRUMP HAS BEEN JUDGED GUILTY AND TAKEN TO PRISON" O "TRUMP HAS BEEN JUDGED GUILTY AND NOW IS IN PRISON"  (PROVARE AD USARE IL TAG_ DEL VERBO)
        for cond_token in cond_tokens:
            cond_predicate = library.get_predicate(cond_token, predicates)
            if cond_predicate.dep_token == conj_head:
                library.make_predicate(predicates, cond_token, token)
                break
        if token_predicate is not None:
            if target_token in passive_tokens and token_predicate.obj_token_list == [] and token_predicate.subj_token_list == []:
                token_predicate.obj_token_list = target_predicate.obj_token_list
            elif target_token not in passive_tokens and token not in passive_tokens and token_predicate.subj_token_list == []:
                token_predicate.subj_token_list = target_predicate.subj_token_list
        else:
            if target_token in passive_tokens:
                library.make_predicate(predicates, token, token, None, target_predicate.obj_token_list)
            else:
                library.make_predicate(predicates, token, token, None, target_predicate.subj_token_list)
    elif conj_head.dep_ is "xcomp":
        if not library.add_to_prefix(conj_head.head, token, predicates):
            head_predicate = library.get_predicate(until_not("xcomp", conj_head), predicates)
            library.make_predicate(predicates, token, token, head_predicate.subj_token_list, None, None, conj_head.head)
    elif conj_head.dep_ is "attr" or target_token.dep_ is "nsubj" or target_token.dep_ is "nsubjpass" or target_token.dep_ is "dobj" or target_token.dep_ is "acomp":
        library.add_to_same_var_list(target_token, token, variables, predicates, num_of_terms)
    elif conj_head.dep_ in dep_modifiers:
        if not library.get_predicate(token, predicates):
            target_predicate = library.get_predicate(target_token, predicates)
            library.make_predicate(predicates, token, target_predicate.dep_token)
    elif conj_head.dep_ is "pobj":
        prep_token = conj_head.head
        if prep_token.dep_ is "agent":
            prep_head = prep_token.head
            library.add_to_subj_list(token, prep_head, variables, predicates, num_of_terms)

def dep_csubj(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token.dep_ is "aux" or target_token.dep_ is "auxpass":
        target_token = target_token.head
    token_predicate = library.get_predicate(token, predicates)
    target_predicate = library.get_predicate(target_token, predicates)
    if target_predicate is not None:
        target_predicate.subj_token_list = token_predicate.obj_token_list
    else:
        library.make_predicate(predicates, target_token, target_token, token_predicate.obj_token_list)

def dep_csubjpass(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token.dep_ is "aux" or target_token.dep_ is "auxpass":
        target_token = target_token.head
    token_predicate = library.get_predicate(token, predicates)
    target_predicate = library.get_predicate(target_token, predicates)
    if target_predicate is not None:
        target_predicate.subj_token_list = token_predicate.subj_token_list
    else:
        library.make_predicate(predicates, target_token, target_token, token_predicate.subj_token_list)

def dep_dobj(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token.dep_ is "xcomp":
        target_token = library.until_not("xcomp", target_token)
    if not library.add_to_obj_list(token, target_token, variables, predicates, num_of_terms):
        library.make_predicate(predicates, target_token, target_token, None, token)
    library.make_mono_predicate(token, predicates)

def dep_nsubj(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if target_token.dep_ is not "parataxis":
        if target_token.dep_ is "ccomp":
            if not library.add_to_subj_list(token, target_token, variables, predicates, num_of_terms):
                library.make_predicate(predicates, target_token, target_token, token)
        elif target_token.dep_ is "relcl":
            if not library.add_to_subj_list(target_token.head, target_token, variables, predicates, num_of_terms):
                library.make_predicate(predicates, target_token, target_token, target_token.head)
        else:
            if not library.add_to_subj_list(token, target_token, variables, predicates, num_of_terms):
                library.make_predicate(predicates, target_token, target_token, token)
            library.make_mono_predicate(token, predicates)

def dep_nsubjpass(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    if not library.add_to_obj_list(token, target_token, variables, predicates, num_of_terms):
        library.make_predicate(predicates, target_token, target_token, None, token)

def dep_oprd(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    target_token = token.head
    target_predicate = library.get_predicate(target_token, predicates)

    if target_token in passive_tokens:  #LA FALLA STA IN DUE VERBI AL PASSIVO UNITI DA UNA CONGIUNZIONE
        if not library.get_predicate(token, predicates) and target_predicate.obj_token_list != []:
            library.make_predicate(predicates, token, target_predicate.obj_token_list[0])
    else:
        if not library.get_predicate(token, predicates) and target_predicate.subj_token_list != []:
            library.make_predicate(predicates, token, target_predicate.subj_token_list[0])

def dep_pcomp(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    prep_token = token.head
    prep_head = prep_token.head
    if prep_head.dep_ is "xcomp":
        prep_head = library.until_not("xcomp", prep_head)
    if library.get_predicate(prep_token, predicates) is None:
        library.make_mono_predicate(token, predicates)
        library.make_predicate(predicates, prep_token, prep_head, token)

def dep_pobj(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if token.dep_ is "conj":
        pobj_token = library.until_not("conj", token)
        prep_token = pobj_token.head
    else:
        prep_token = token.head

    if prep_token.dep_ is "prt":
        target_token = prep_token.head
        if target_token.dep_ is "xcomp":
            target_token = library.until_not("xcomp", target_token)
        if not library.add_to_obj_list(token, target_token, variables, predicates, num_of_terms):
            library.make_predicate(predicates, target_token, target_token, None, token)
        library.make_mono_predicate(token, predicates)
    else:
        if prep_token.dep_ is "conj":
            prep_head = library.until_not("conj", prep_token)
            prep_head = prep_head.head
        else:
            prep_head = prep_token.head

        if prep_head.dep_ is "appos":
            prep_head = library.until_not("appos", prep_head)
        elif prep_head.dep_ is "xcomp":
            prep_head = library.until_not("xcomp", prep_head)
        #elif prep_head.dep_ is "conj":
        #    prep_head = until_not("conj", prep_head)
        if prep_token.dep_ is "agent":
            library.add_to_subj_list(token, prep_head, variables, predicates, num_of_terms)
            while prep_head.dep_ is "conj" and prep_head.head in passive_tokens:
                library.add_to_subj_list(token, prep_head.head, variables, predicates, num_of_terms)
                prep_head = prep_head.head

        elif library.get_predicate(prep_token, predicates) is None:
            library.make_mono_predicate(token, predicates)
            library.make_mono_predicate(prep_head, predicates)
            library.make_predicate(predicates, prep_token, prep_head, token)

def dep_prep(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if token.head in isa_tokens and (token.text == "of" or token.text == "by"):
        isa_tokens.append(token)

def dep_relcl(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if library.get_predicate(token, predicates) is None:
        library.make_predicate(predicates, token, token, token.head)
    else:
        library.add_to_subj_list(token.head, token, variables, predicates, num_of_terms)

def dep_root(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if token.lemma_ == "be":
        isa_tokens.append(token)
    elif token.lemma_ == "make":
        for child in token.children:
            if child.text == "of" or child.text == "by":
                isa_tokens.append(token)
                break

def dep_xcomp(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    library.add_to_prefix(token, token.head, predicates)

def dep_scarta(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    pass

def dep_switcher(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    switcher = {
    "acl": dep_acl, #ES. There are many online sites offering booking facilities ("offering" è acl di "sites")
    "acomp": dep_dobj, #ES. You are so beautiful ( "beautiful" è acomp di "are")
    #"advcl": dep_advcl, #---- TO-DO ---- #ES. I wasn't sure if she liked me ( "liked" è advcl di "was"), She came to see me ("see" è il advcl di "came")
    "advmod": dep_advmod, #ES. She is alredy here ("alredy" è advmod di "is" e "here" è advmod di "is")
    #"agent": dep_agent, #GESTITA DA POBJ #ES. The car was bought by Sam ( "Sam" è pobj di "by" e "by" è agent di "bought")
    "amod": dep_modifier, #ES. A nice girl ("nice" è amod di "girl")
    "appos": dep_modifier, #ES. John, my brother ("brother" è appos di "John")
    "attr": dep_dobj, #ES. He is a student ("student" è attr di "is")
    #"aux": dep_aux, #SCARTATA
    "auxpass": dep_auxpass, #SCARTATA
    #"case": dep_case, #SCARTATA #ES. John's car ("'s" è case di "John")
    #"cc": dep_cc, #SCARTATA #ES. John, Mary and Sam ("and" è cc di "John")
    "ccomp": dep_ccomp, #ES. She said that she wanted to go ("wanted" è ccomp di "said")
    "compound": dep_compound,
    "conj": dep_conj,
    "csubj": dep_csubj,
    "csubjpass": dep_csubjpass,
    "dative": dep_modifier,
    #"dep": dep_dep, #SCARTATA #Una dipendenza non classificata
    #"det": dep_det, #SCARTATA #ES. The US military ("The" è det di "military")
    "dobj": dep_dobj,
    #"expl": dep_expl, #SCARTATA
    #"intj": dep_intj, #SCARTATA
    "mark": dep_advmod, #ES. She came as she promised ("as" è mark di "promised")
    #"meta": dep_meta, #SCARTATA #Mete informazioni ES. (Applause) Thank you  ("Applause" è meta di "Thank")
    "npadvmod": dep_modifier,  #ES. A five years old girl ("five" è nummod di "years", "year" è npadvmod di "old" e "old" è amod di "girl" )
    #"neg": dep_neg, #SCARTATA #ES. She decided not to come ("not" è neg di "come")
    "nmod": dep_modifier, #Un modificatore non classificato
    "npmod": dep_modifier,
    "nsubj": dep_nsubj,
    "nsubjpass": dep_nsubjpass,
    "nummod": dep_modifier, #ES. 14 degrees ("14" è nummod di "degrees"), Two dozens ("Two" è nummod di "dozens")
    "oprd": dep_oprd, #XXXXX TO-DO XXXXX #MODIFICA UN EVENTO MA PUò ESSERE UN SOSTANTIVO CHE PUò A SUA VOLTA AVERE DEI MODIFICATORI... ES. I am considered her best friend ("friend" è l'oprd di "considered" ma "her" e "best" sono modificatori di "friend")
    #"parataxis": dep_parataxis, #SCARTATA # She, I mean, Mary was here ("mean" è parataxis di "was")
    "pcomp": dep_pcomp, #POTREI ANCHE USARE DEP_POBJ #ES. I agree with what you said ("said" è pcomp di "with" e "with" è prep con "agree")
    "pobj": dep_pobj,  #ES. Thank you for coming to my house ("house" è pobj di "to" e "to" è prep di "coming")
    "poss": dep_modifier, #ES. John's car ("John" è poss di "car")
    #"preconj": dep_preconj, #SCARTATA #ES- Either John or Mary ("Either" è preconj di "John"), Not only John but also Mary ("Not" è preconj di "John")
    "predet": dep_modifier, #ES. All the books we read ("All" è predet di "books")
    "prep": dep_prep, #ES. Thank you for coming to my house ("house" è pobj di "to" e "to" è prep di "coming")
    "prt": dep_modifier, #ES. Shut down the machine ("down" è prt di "shut")
    #"punct": dep_punct, #SCARTATA
    "quantmod": dep_modifier, #ES. Two to three dozens ("Two" è quantmod di "dozens" e "to" è quantmod di "dozens")
    "relcl": dep_relcl,
    "ROOT": dep_root,
    "xcomp": dep_xcomp
    }
    # Get the function from switcher dictionary
    func = switcher.get(token.dep_, lambda token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens: dep_scarta)
    # Execute the function
    func(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens)
