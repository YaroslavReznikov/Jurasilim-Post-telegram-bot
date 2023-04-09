import parsing
try:
    pars = parsing.parsing_part()
    pars.get_links()
except:
    pass

finally:
    print("All new news were addded")
    del pars
