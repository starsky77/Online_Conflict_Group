from colorama import Fore, Back, Style, init

init(autoreset=True)

with open('colored_text.txt', 'w') as f:
    f.write(Fore.RED + 'This is red text.\n')
    f.write(Fore.GREEN + 'This is green text.\n')
    f.write(Fore.BLUE + 'This is blue text.\n')

    f.write(Back.YELLOW + 'This is text with a yellow background.\n')
    f.write(Back.CYAN + 'This is text with a cyan background.\n')
    f.write(Back.MAGENTA + 'This is text with a magenta background.\n')

    f.write(Fore.RED + Back.YELLOW + 'This is red text on a yellow background.\n')

    f.write(Style.BRIGHT + 'This is bright text.\n')
    f.write(Style.DIM + 'This is dim text.\n')
    f.write(Style.NORMAL + 'This is normal text.\n')
