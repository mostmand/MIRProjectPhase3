def get_input_from_user():
    while True:
        print('Please select one of the options below:')
        print('1.Crawl')
        print('2.Remove elastic index')
        print('3.Index jsons into elastic')
        print('4.Calculate PageRank and index it into elastic')
        print('5.Search')
        print('0.Exit')
        try:
            inp = int(input())
            if inp == 0:
                break
            yield inp
        except:
            print('Your input is not recognized')


for inp in get_input_from_user():
    print(inp)
    if inp == 1:
        pass
    elif inp == 2:
        pass
    elif inp == 3:
        pass
    elif inp == 4:
        pass
    elif inp == 5:
        pass
