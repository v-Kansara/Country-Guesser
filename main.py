import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageSequence, ImageTk
from countryInfo import *
from countryFlags import *
import random
import math


class CountryGuessingGame:

    def __init__(self):
        self.root = tk.Tk()

        self.title = self.root.title("Country Guessing Game")

        self.geometry = self.root.geometry("1125x700")

        self.bgColor = self.root.configure(bg="black")

        self.mainLabel = tk.Label(self.root,
                                  text="Country Guesser™",
                                  font=("MS Sans Serif", 20),
                                  fg="white",
                                  bg="black")
        self.mainLabel.pack(padx=10, pady=10)

        self.play_gif()

        self.playButton = tk.Button(self.root,
                                    text="Play Country Guesser",
                                    command=self.startGame)
        self.playButton.pack(padx=10, pady=10)

        self.helpButton = tk.Button(self.root,
                                    text="How to Play",
                                    command=self.howToPlay)
        self.helpButton.pack(padx=10, pady=10)

        #self.textbox = tk.Text(self.root, height=5, font=('Arial', 10))
        #self.textbox.pack(padx=10, pady=10)

        self.countryCounter = 0

        self.root.mainloop()

    # startGame - Starts the game and prompts user to enter difficulty level
    def startGame(self):
        self.playButton.destroy()
        self.helpButton.destroy()

        self.options = ["Easy", "Medium", "Hard"]

        self.clicked = tk.StringVar()
        self.clicked.set(self.options[0])

        self.difficultyLabel = tk.Label(self.root,
                                        text="Choose Your Difficulty Level",
                                        font=("MS Sans Serif", 12),
                                        fg="white",
                                        bg="black")
        self.difficultyLabel.pack(padx=10, pady=5)

        self.dropdown = tk.OptionMenu(self.root, self.clicked, *self.options)
        self.dropdown.pack(padx=10, pady=10)

        self.confirmButton = tk.Button(self.root,
                                       text="Confirm Selection",
                                       command=self.confirmMessage)
        self.confirmButton.pack(padx=10, pady=10)

    # guessCountry - Allows user to guess the country
    def guessCountry(self):
        self.my_entry = tk.Entry(self.root,
                                 text="Start Typing...",
                                 font=("MS Sans Serif", 20))
        self.my_entry.pack()

        self.my_list = tk.Listbox(self.root, width=40, height=10)
        self.my_list.pack(pady=10)

        self.countries = AllCountriesInWorld

        self.update(self.countries)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)

        self.my_entry.bind("<KeyRelease>", self.check)

    # showFacts - Shows the facts about the random country
    def showFacts(self, difficultyLevel):
        self.line = tk.Label(self.root,
                             text="───────────────────────────────────────",
                             font=("MS Sans Serif", 12),
                             fg="#fff",
                             bg="#000")
        self.line.pack(padx=10, pady=0)
        self.countryIndex = Countries.index(random.choice(Countries))
        self.displayCountry(self.countryIndex, difficultyLevel)

    # howToPlay - Gives info on how to play the game
    def howToPlay(self):
        self.helpMessage = messagebox.showinfo(
            title="How To Play Country Guesser",
            message=
            "1. To play Country Guesser, click the play game button. It will send you to a screen that will prompt you for a difficulty level. \n2. Choose a level out of the options, easy, medium or hard, and confirm your choice by following the steps. \n3. Then, it will pop up a box where you can enter your guess for the country."
        )

    def show(self):
        self.myLabel = tk.Label(self.root, text=self.clicked.get())
        self.myLabel.pack()

    # confirmSelection - Sets the user's difficulty level
    def confirmSelection(self):
        self.difficultyLabel.config(text="Difficulty Level: " +
                                    self.clicked.get())
        self.difficultyLabel.pack(padx=10, pady=0)
        self.difficulty = self.clicked.get()
        self.dropdown.destroy()
        self.confirmButton.destroy()
        self.showFacts(self.difficulty)

    # confirmMessage - Prompts user if they want to confirm difficulty level
    def confirmMessage(self):
        self.messageBox = messagebox.askyesno(
            title="Confirm Difficulty Level",
            message="Do you wish to confirm the " + self.clicked.get() +
            " difficulty level?")
        if self.messageBox:
            self.confirmSelection()

    # Update the listbox
    def update(self, data):
        # Clear the listbox
        self.my_list.delete(0, tk.END)

        # Add countries to listbox
        for item in data:
            self.my_list.insert(tk.END, item)

    # Update entry box with listbox clicked
    def fillout(self, e):
        # Delete whatever is in the entry box
        self.my_entry.delete(0, tk.END)

        # Add clicked list item to entry box
        self.my_entry.insert(0, self.my_list.get(tk.ANCHOR))

    # Create function to check entry vs listbox
    def check(self, e):
        # grab what was typed
        typed = self.my_entry.get()
        if typed == '':
            data = self.countries
        else:
            data = []
            for item in self.countries:
                if typed.lower().capitalize() in item.lower().capitalize():
                    data.append(item)

        # Update listbox with selected items
        self.update(data)

    def play_gif(self):
        global img
        img = Image.open("earth.gif")
        self.lbl = tk.Label(self.root, borderwidth=0, background='#000')
        self.lbl.place(x=80, y=20)

        for img in ImageSequence.Iterator(img):
            img = img.resize((175, 175))
            img = ImageTk.PhotoImage(img)
            self.lbl.config(image=img)

            self.root.update()
        self.root.after(0, self.play_gif)

    # displayCountry function to show the facts of the country (Based on Difficulty Level)
    def displayCountry(self, countryIndex, difficultyLevel):
        # Population
        self.countryPop = tk.Label(self.root,
                                   text="Country Population (2022): " +
                                   str(Population[countryIndex]),
                                   fg="#fff",
                                   bg="#000")
        self.countryPop.pack(padx=10, pady=5)
        # Country Size
        self.countrySize = tk.Label(self.root,
                                    text="Country Size (Sq Mi): " +
                                    str(Size[countryIndex]),
                                    fg="#fff",
                                    bg="#000")
        self.countrySize.pack(padx=10, pady=5)
        # Currency
        self.countryCurrency = tk.Label(
            self.root,
            text="Country Currency (Currency Type + symbol): " +
            str(Currency[countryIndex]),
            fg="#fff",
            bg="#000")
        self.countryCurrency.pack(padx=10, pady=5)

        if difficultyLevel == "Medium":
            # Capital
            self.countryCapital = tk.Label(self.root,
                                           text="Country Capital: " +
                                           str(Capital[countryIndex]),
                                           fg="#fff",
                                           bg="#000")
            self.countryCapital.pack(padx=10, pady=5)
            # Time Zones
            self.countryTimeZones = tk.Label(
                self.root,
                text=
                "Country's Total Number of Time Zones (Mainland Country, No Islands or Territories): "
                + str(NumTimeZones[countryIndex]),
                fg="#fff",
                bg="#000")
            self.countryTimeZones.pack(padx=10, pady=5)

        if difficultyLevel == "Easy":
            # Capital
            self.countryCapital = tk.Label(self.root,
                                           text="Country Capital: " +
                                           str(Capital[countryIndex]),
                                           fg="#fff",
                                           bg="#000")
            self.countryCapital.pack(padx=10, pady=5)
            # Time Zones
            self.countryTimeZones = tk.Label(
                self.root,
                text=
                "Country's Total Number of Time Zones (Mainland Country, No Islands or Territories): "
                + str(NumTimeZones[countryIndex]),
                fg="#fff",
                bg="#000")
            self.countryTimeZones.pack(padx=10, pady=5)
            # National Language
            self.countryLanguage = tk.Label(
                self.root,
                text="Country National Language: " +
                str(NationalLanguage[countryIndex]),
                fg="#fff",
                bg="#000")
            self.countryLanguage.pack(padx=10, pady=5)
            # GDP
            self.countryGDP = tk.Label(self.root,
                                       text="Country GDP (2021)($): " +
                                       str(GDP[countryIndex]),
                                       fg="#fff",
                                       bg="#000")
            self.countryGDP.pack(padx=10, pady=5)

        self.guessLine = tk.Label(
            self.root,
            text="───────────────────────────────────────",
            font=("MS Sans Serif", 12),
            fg="#fff",
            bg="#000")
        self.guessLine.pack(padx=10, pady=0)

        self.guessLabel = tk.Label(self.root,
                                   text="Guess The Country",
                                   font=("MS Sans Serif", 12),
                                   fg="#fff",
                                   bg="#000")
        self.guessLabel.pack(padx=10, pady=(0, 10))
        self.guessCountry()

        # Assign Level
        if difficultyLevel == "Easy":
            self.Level = 5
        elif difficultyLevel == "Medium":
            self.Level = 4
        elif difficultyLevel == "Hard":
            self.Level = 3

        #print("Mystery Country's Flag: ")
        #print()
        #for item in CountryFlags[countryIndex]:
        #    print(item)
        #print()
        #time.sleep(1)

        self.GUESSButton = tk.Button(
            self.root,
            text="Guess!",
            command=lambda: self.checkCountry(difficultyLevel))
        self.GUESSButton.pack(padx=10, pady=10)

    def checkCountry(self, difficultyLevel):
        if self.countryCounter <= (self.Level - 1):
            if self.my_entry.get() in AllCountriesInWorld:
                self.targetCountryIndex = AllCountriesInWorld.index(
                    Countries[self.countryIndex])
                self.CountryName = AllCountriesInWorld[self.targetCountryIndex]
                inputCountryIndex = AllCountriesInWorld.index(
                    self.my_entry.get())
                inputCountryCapital = AllCapitalsInWorld[inputCountryIndex]
                targetLat = AllCapitalLocations[self.targetCountryIndex][0]
                targetLong = AllCapitalLocations[self.targetCountryIndex][1]
                inputCountryLat = AllCapitalLocations[inputCountryIndex][0]
                inputCountryLong = AllCapitalLocations[inputCountryIndex][1]

                if self.my_entry.get().lower() == self.CountryName.lower():
                    self.InfoBox = messagebox.showinfo(
                        title="You Guessed Correctly!",
                        message=
                        "Congrats, you guessed the correct country! The mystery country was "
                        + self.CountryName + "!")
                    self.GUESSButton.config(text="End Game",
                                            command=lambda: self.endGame())
                else:  # Runs if user entered an incorrect country
                    self.countryCounter += 1
                    if self.Level == 3:
                        self.InfoBox = messagebox.showinfo(
                            title="You Guessed Incorrectly!",
                            message=
                            "Sorry, that is not the correct country! Please try again! You have "
                            + str((self.Level) - self.countryCounter) +
                            " tries left!")
                    elif self.Level == 4 or self.Level == 5:
                        self.InfoBox = messagebox.showinfo(
                            title="You Guessed Incorrectly!",
                            message=
                            "Sorry, that is not the correct country! Please try again! You have "
                            + str((self.Level) - self.countryCounter) +
                            " tries left! The capital of the mystery country ("
                            + AllCapitalsInWorld[self.targetCountryIndex] +
                            ") is " + str(
                                round(
                                    self.calcDistanceBetween(
                                        targetLat, inputCountryLat, targetLong,
                                        inputCountryLong))) +
                            " miles away from the capital of " +
                            self.my_entry.get() + " (" + inputCountryCapital +
                            ").")
                    if self.countryCounter == (self.Level):
                        if self.Level == 4 or self.Level == 5:
                            self.endBox = messagebox.showinfo(
                                title="You Couldn't Guess The Correct Country!",
                                message=
                                "Unfortunately, you were not able to guess the correct country in "
                                + str(self.Level) +
                                " guesses on the easy or medium difficulty level! The mystery country was "
                                + self.CountryName +
                                ". Please try again next time!")
                            self.GUESSButton.config(
                                text="End Game",
                                command=lambda: self.endGame())
                        else:
                            self.endBox = messagebox.showinfo(
                                title="You Couldn't Guess The Correct Country!",
                                message=
                                "Unfortunately, you weren't able to guess the correct country. You chose the hard difficulty level, so the mystery country will not be displayed. Good luck next time!"
                            )
                            self.GUESSButton.config(
                                text="End Game",
                                command=lambda: self.endGame())
            else:  # Runs if user did not enter a valid country
                self.warningBox = messagebox.showerror(
                    title="Invalid Country",
                    message="Please enter a valid country.")

    def calcDistanceBetween(self, lat1, lat2, long1, long2):
        a = (math.sin(((lat2 - lat1) * (math.pi / 180)) / 2)**2) + (math.cos(
            (lat1 * (math.pi / 180))) * math.cos(
                (lat2 * (math.pi / 180))) * (math.sin(
                    ((long2 - long1) * (math.pi / 180)) / 2)**2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distanceBetween = (3958.756) * c
        return distanceBetween

    def endGame(self):
        self.endMessage = messagebox.askyesno(
            title="End Game",
            message=
            "Would you like to restart the game or end it? Click YES to restart or NO to end it."
        )
        if self.endMessage:
            self.root.destroy()
            CountryGuessingGame()
        elif not self.endMessage:
            self.root.destroy()


# CALL
CountryGuessingGame()
