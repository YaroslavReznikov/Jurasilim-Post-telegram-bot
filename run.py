from main import main



does_work = False

if not does_work:
    does_work = True
    try:
        main()
    except:
        does_work = False