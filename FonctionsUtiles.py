# Fonction ensemble
    # Renvoie une liste avec aucun doublon
def ensemble(l):
    res = list()
    for e in l:
        if not e in res:
            res.append(e)
    return res

def splitlist(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]