import parsing

pars = parsing.ParsingPart()

try:
    pars.get_links()
except:
    pass

finally:
    del pars
