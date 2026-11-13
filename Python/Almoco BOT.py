def chooseBrowser():
    browsers = ["Chrome", "Firefox", "Edge"]

    while True:
        print("Escolha o navegador que deseja usar:")
        for i, browser in enumerate(browsers):
            print(f"{i + 1}. {browser}")
            
        choice = int(input("Escolha o número do navegador: "))
        if 1 <= choice <= len(browsers):
            return browsers[choice - 1]
            break
        else:
            print(f"\n /!\ Escolha inválida. Por favor, tente novamente. /!\ \n")
            continue


    chooseBrowser()