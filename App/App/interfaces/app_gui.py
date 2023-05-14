class GUI:
    def _init_(self):
        pass

    def startApp(self):
        text = "Welcome to Hawwkstore!"

        print("\n\033[2mStarting app...\033[0m\n\n")
        print("\033[94m")

        for _ in range(len(text)):
            print("*", end='')

        print("\n\033[96m" + "\033[1m" + text + "\033[0m" + "\033[94m")

        for _ in range(len(text)):
            print("*", end='')

        print("\033[0m\n")

    def exitApp(self):
        text = "Thank you for using Hawwkstore!"

        print("\n\n\033[94m")

        for _ in range(len(text)):
            print("*", end='')

        print("\n\033[96m" + "\033[1m" + text + "\033[94m")

        for _ in range(len(text)):
            print("*", end='')

        print("\033[0m")
        print("\n\n\033[2mExiting app...\033[0m\n")

    def back(self):
        print("\n\033[2mReturning to previous menu ...\033[0m\n")

    def welcomeSession(self, name):
        print("\033[132m" + "\033[92m" + "\n*** Hello " +
              "\033[1m" + name.split(" ")[0] + "! ***\033[0m")

    def exitSession(self, name):
        print("\033[132m" + "\033[92m" + "Thank you " + "\033[1m" + name.split(" ")
              [0] + "\033[0m" + "\033[92m" + "! We hope to see you soon!")

    def title(self, text):
        print("\n\033[1m" + "\033[95m" + text + "\033[0m\n")

    def subtitle(self, text):
        print(f'\033[1m{text}\033[0m')

    def subtitleForOptions(self):
        print("\033[1mPlease select the desired option:\033[0m")

    def options(self, optionList: list):
        for i in range(len(optionList)):
            print(f"\t{i+1}). {optionList[i]}")

        print()

    def prompt(self):
        print("->", end=" ")

    def errorLog(self, error):
        self.subtitle("\n\033[1m\033[31m[ERROR]: " + error + "!\033[0m\n")

    def infoLog(self, text):
        self.subtitle("\n\033[34m[INFO]: " + text + "\n")

    def warningLog(self, text):
        self.subtitle("\n\033[36m[ALERT]: " + text + "!\n")

    def tryAgain(self, text):
        print("\033[2m" + text + " ...\033[0m\n")

    def tryAgain(self):
        print("\033[2mPlease try again ...\033[0m\n")
