import parsing

pars = parsing.parsing_part()

try:
    pars.get_links()
except:
    pass

finally:
    pars.database.database.close()
