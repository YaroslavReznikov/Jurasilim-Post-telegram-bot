from main import main



does_work = False

if not does_work:
    does_work = True
    try:
        main()
    except Exception as exsp:
        print(exsp)
        does_work = False