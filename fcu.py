# Fonction ensemble
    # Renvoie une liste avec aucun doublon
def ensemble(l):
    res = list()
    for e in l:
        if not e in res:
            res.append(e)
    return res