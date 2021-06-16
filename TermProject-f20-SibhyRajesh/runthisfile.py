## Sibhy Rajesh
## Term Project 15-112

from datascraper import *
from players import *
from draftAlgorithms import *
from cmu_112_graphics import * # from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
import string
import copy

## This file contains all the UI and other related features. 
## running this file should run the app


# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
# used course notes for learning the modal app and 
# some parts of the Modal App framework from there

class splashPageMode(Mode): # from source

    def appStarted(self):
        self.originalImage = self.loadImage('termprojectsplashpage.png')
        self.splashPageImage = self.scaleImage(self.originalImage, self.width/self.originalImage.size[0])

    def redrawAll(self, canvas): 
        ## Old Splash Page
        # font = 'STIXVariants 18 bold'
        # canvas.create_text(mode.width/2, 150, text='Fantasy Football Draft Practicer', font=font)
        # canvas.create_text(mode.width/2, 250, text='Press any key to start!', font=font)
        
        ## New Splash Page
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.splashPageImage))
    
    def keyPressed(self, event):
        if event.key == "0":
            self.app.setActiveMode(self.app.playerLookupMode)
        elif event.key == "-":
            self.app.setActiveMode(self.app.selectionMode)
        elif event.key != "Escape":
            self.app.setActiveMode(self.app.helpMode)
        

class selectionMode(Mode):

    def appStarted(mode):
        numModes = 4
        yinc = mode.height/numModes
        
        # sets dimensions for different buttons
        mode.autoDraftButtonDim = [0,0, mode.width/2, yinc]
        mode.posDraftButtonDim = [0, yinc, mode.width/2, 2*yinc]
        mode.advDraftButtonDim = [0, 2*yinc, mode.width/2, 3*yinc]
        mode.minimaxDraftButtonDim = [0, 3*yinc, mode.width/2, 4*yinc]

        mode.originalImage = mode.loadImage('draftSelectionPage.png')
        mode.backgroundImage = mode.scaleImage(mode.originalImage, mode.width/mode.originalImage.size[0])
    
    def keyPressed(mode, event):
        if event.key == 'Escape':
            mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas): 
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.backgroundImage))
        # selectionMode.drawButtons(mode, canvas)

    def drawButtons(mode, canvas):
        numModes = 4
        yinc = mode.height/numModes
        (x0,y0,x1,y1) = [0, 0, mode.width/2, yinc]

        for i in range(numModes):
            canvas.create_rectangle(x0, y0, x1, y1, fill = "red", width = 5, 
            outline = "Black")
            y0 += yinc
            y1 += yinc

    ## Old Button Design - Deprecated
    # def autoDraftButton(mode, canvas):
    #     (x0,y0,x1,y1) = mode.autoDraftButtonDim
    #     canvas.create_rectangle(x0, y0, x1, y1, fill = "Red", width = 0)
    #     midX = (x0 + x1)/2
    #     midY = (y0 + y1)/2 
    #     canvas.create_text(midX, midY, text = "Greedy Draft", font = mode.font)

    # def posDraftButton(mode, canvas):
    #     (x0,y0,x1,y1) = mode.posDraftButtonDim
    #     canvas.create_rectangle(x0, y0, x1, y1, fill = "Green", width = 0)
    #     midX = (x0 + x1)/2
    #     midY = (y0 + y1)/2 
    #     canvas.create_text(midX, midY, text = "Positional Draft", font = mode.font)

    # def advDraftButton(mode, canvas):
    #     (x0,y0,x1,y1) = mode.advDraftButtonDim
    #     canvas.create_rectangle(x0, y0, x1, y1, fill = "Deep Pink", width = 0)
    #     midX = (x0 + x1)/2
    #     midY = (y0 + y1)/2 
    #     canvas.create_text(midX, midY, text = "Adversarial Draft", font = mode.font)
        
    # def minimaxDraftButton(mode, canvas):
    #     (x0,y0,x1,y1) = mode.minimaxDraftButtonDim
    #     canvas.create_rectangle(x0, y0, x1, y1, fill = "DeepSkyBlue", width = 0)
    #     midX = (x0 + x1)/2
    #     midY = (y0 + y1)/2 
    #     canvas.create_text(midX, midY, text = "Minimax Draft", font = mode.font)
    
    def mousePressed(mode, event):
        if selectionMode.pressedInButton(event.x, event.y, mode.autoDraftButtonDim):
            mode.app.draftType = 0
            mode.app.setActiveMode(mode.app.draftMode) 

        elif selectionMode.pressedInButton(event.x, event.y, mode.posDraftButtonDim):
            mode.app.draftType = 1
            mode.app.setActiveMode(mode.app.draftMode)

        elif selectionMode.pressedInButton(event.x, event.y, mode.advDraftButtonDim):
            mode.app.draftType = 2
            mode.app.setActiveMode(mode.app.draftMode)

        elif selectionMode.pressedInButton(event.x, event.y, mode.minimaxDraftButtonDim):
            mode.app.draftType = 3
            mode.app.setActiveMode(mode.app.draftMode)
        
    def pressedInButton(x,y, buttonDim):
        if buttonDim[0] < x < buttonDim[2]:
            if buttonDim[1] < y < buttonDim[3]:
                return True
        return False

class draftMode(Mode):

    def redrawAll(self, canvas):
        draftMode.checkImage(self)
        # canvas.create_text(self.width/8, 0, 
        # text = "Player Lookup",
        # font = "STIXVariants 20 bold", anchor = "nw")

        # canvas.create_text(self.width/8, self.height/10, 
        # text = "Click on a player name\n to view their stats",
        # font = "STIXVariants 14 bold", anchor = "nw")
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.backgroundImage))

        # autoDraftMode.drawGrid(self, canvas)
        if not self.app.draftType == 3:
            draftMode.drawSearchBar(self, canvas, self.searchBarDim, 1)
        else:
            self.searchContents = "2"

        draftMode.drawSearchBar(self, canvas, self.searchBarDim2, 2)
        draftMode.drawSubmitButton(self, canvas)

        interval = 5
        if self.timer % interval == 0 and self.searchBarMode:
            draftMode.drawSearchBarIcon(self, canvas, self.searchBarIconDim)
        elif self.timer % interval == 0 and self.searchBarMode == False:
            draftMode.drawSearchBarIcon(self, canvas, self.searchBarIconDim2)
    
    def appStarted(self):
        self.numberOfPlayers = 12
        defaultRoster = {"qb": set(), "wr": set(), "rb":set(), "te": set()}
        rosters = [copy.deepcopy(defaultRoster) for i in range(self.numberOfPlayers)]
        self.defaultSuggestions = getSuggestedPlayers(rosters[0], Player.allPlayers, 
        rosters)
        self.selectedPlayer = None
        self.searchBarMode = False
        self.searchContents = ""
        self.searchContents2 = ""
        self.sbm = min(self.width,self.height)/30 # sbm means search bar margin
        self.searchBarDim = [self.width/4 - self.sbm*4, self.height/2 -self.sbm, self.width/4 + self.sbm*4, self.height/2 + self.sbm ]
        self.searchBarDim2 = []
        self.margin = 150
        for i in range(len(self.searchBarDim)):
            if i % 2 == 1:
                self.searchBarDim2.append(self.searchBarDim[i] + self.margin)
            else:
                self.searchBarDim2.append(self.searchBarDim[i])
        self.searchOutput = None
        self.searchBarIconDim  =  [self.searchBarDim[0], self.searchBarDim[1], self.searchBarDim[0] + self.searchBarDim[2] * 0.01, self.searchBarDim[3]]
        self.searchBarIconDim2 = [self.searchBarDim2[0], self.searchBarDim2[1], self.searchBarDim2[0] + self.searchBarDim2[2] * 0.01, self.searchBarDim2[3]]
        self.origIconDim = copy.deepcopy(self.searchBarIconDim)
        self.origIconDim2 = copy.deepcopy(self.searchBarIconDim2)
        self.displayedPlayers = self.defaultSuggestions
        draftMode.checkImage(self)   
      
       

        self.timer = 0
        self.droppedMargin = 150
        self.submitButton = [self.width/2 + self.margin/3, self.height/2 - self.margin , self.width, self.height - self.margin]

        # for i in range(len(self.searchBarDim)):
        #     if i % 2 == 1:
        #         self.submitButton.append(self.searchBarDim[i] + self.droppedMargin)
        #     else:
        #         self.submitButton.append(self.searchBarDim[i] + self.width/3)
    
    def checkImage(self):
        
        if self.app.draftType == 0:
            self.originalImage = self.loadImage('autodraftmode.png')
        elif self.app.draftType == 1:
            self.originalImage = self.loadImage('posdraftmode.png')
        elif self.app.draftType == 2:
            self.originalImage = self.loadImage('adversarialdraftmode.png')
        elif self.app.draftType == 3:
            self.originalImage = self.loadImage('minimaxdraftmode.png')
        self.backgroundImage = self.scaleImage(self.originalImage, self.width/self.originalImage.size[0])

    def drawSubmitButton(self, canvas):
        x0, y0, x1, y1 = self.submitButton
        # canvas.create_rectangle(x0, y0, x1, y1, fill = "lightblue")

    def timerFired(self):
        self.searchContents.strip().lower()
        self.timer += 1
        self.displayedPlayers = []
        
        if self.searchContents == "":
            self.displayedPlayers = self.defaultSuggestions
            return

        i = 0
        # len(self.displayedPlayers) < self.numberOfPlayers 
        Player.allPlayers = copy.deepcopy(self.app.playerListCopy)

        while (i < len(Player.allPlayers)):
            if self.searchContents in Player.allPlayers[i].name.lower():
                self.displayedPlayers.append(Player.allPlayers[i])
            i += 1
        
    def drawSearchBarIcon(self, canvas, dim):
        x0, y0, x1, y1 = dim
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
 
    # def drawGrid(self, canvas):
        
    #     x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.defaultSuggestions)))
    #     inc = y1

    #     for i in range(len((self.displayedPlayers))):
    #         canvas.create_rectangle(x0,y0,x1,y1, width = 5, outline = 'White')
    #         midX = (x0 + x1)/2
    #         midY = (y0 + y1)/2
    #         canvas.create_text(midX, midY, text = self.displayedPlayers[i],
    #         font = "STIXVariants 16 bold", fill = 'White')

    #         y0 += inc
    #         y1 += inc

    def drawSearchBar(self, canvas, dim, selected):
        x0, y0, x1, y1 = dim
        canvas.create_rectangle(x0,y0,x1,y1, fill = "lightgreen")
        midX = (x0 + x1)/2
        midY = (y0 + y1)/2
        if selected == 1:
            canvas.create_text(x0, midY, text = self.searchContents,
            font = "STIXVariants 14", anchor = "w")
        else: 
            canvas.create_text(x0, midY, text = self.searchContents2,
            font = "STIXVariants 14", anchor = "w")
            
       
    def keyPressed(self, event):
        if self.searchBarMode:
            tempSearchContents = self.searchContents
        else:
            tempSearchContents = self.searchContents2
        
        if event.key == 'Escape':
            self.app.setActiveMode(self.app.selectionMode)
        if event.key == "Backspace":
            tempSearchContents = tempSearchContents[:-1]
        elif event.key == "Space":
            tempSearchContents += " "
        elif event.key.isdigit():
            tempSearchContents += event.key
    
        if self.searchBarMode:
            self.searchContents = tempSearchContents
        else:
            self.searchContents2 = tempSearchContents
        
         

        iconInc = 8.45*(min(self.width, self.height)/600) # hardcoded to 600 x 600 window, increment for the icon
        self.searchBarIconDim[0] = self.origIconDim[0] + iconInc*len(self.searchContents)
        self.searchBarIconDim[2] = self.origIconDim[2] + iconInc*len(self.searchContents)

        self.searchBarIconDim2[0] = self.origIconDim2[0] + iconInc*len(self.searchContents2)
        self.searchBarIconDim2[2] = self.origIconDim2[2] + iconInc*len(self.searchContents2)
    
    def mousePressed(self, event):
        if self.searchBarDim[0] < event.x < self.searchBarDim[2]:
            if self.searchBarDim[1] < event.y < self.searchBarDim[3]:
                self.searchBarMode = True
        
        if self.searchBarDim2[0] < event.x < self.searchBarDim2[2]:
            if self.searchBarDim2[1] < event.y < self.searchBarDim2[3]:
                self.searchBarMode = False
       
        if self.submitButton[0] < event.x < self.submitButton[2]:
            if self.submitButton[1] < event.y < self.submitButton[3]:
                self.app.numTeams = int(self.searchContents)
                self.app.pick = int(self.searchContents2) % self.app.numTeams
                self.app._root.resizable(True, True)
                self.app.draftChanged = True
                self.app.setActiveMode(self.app.draftResultsMode)
        
            
    

# class posDraftMode(Mode):
    
#     def appStarted(self):
#         self.app.draftType = 1
        # self.numRosters = int(self.getUserInput("Enter number of teams: "))
        # self.pick = int(self.getUserInput("Enter pick number:")) - 1
        # self.customRoster = self.getUserInput("Choose Custom Roster(y/n)? Default is 1 QB, 2 WR, 2 RB, 1 TE")
        # if 'y' in self.customRoster:
        #     self.customQB = int(self.getUserInput("Enter QBs in Roster:"))
        #     self.customRB = int(self.getUserInput("Enter RBs in Roster:"))
        #     self.customWR = int(self.getUserInput("Enter WRs in Roster:"))
        #     self.customTE = int(self.getUserInput("Enter TEs in Roster:"))
        #     self.AIRosters = positionalDraft(self.numRosters, Player.allPlayers,
        #      {"qb": self.customQB, "wr": self.customWR, "rb": self.customRB, "te":self.customTE })
        # else:
        #     self.AIRosters = positionalDraft(self.numRosters, Player.allPlayers)
        # self.displayedPlayers = []

        # for pos in self.AIRosters[self.pick]:
        #     for player in self.AIRosters[self.pick][pos]:
        #         self.displayedPlayers.append(player)
   
    #     self.waitingForInput = False
        
    # def redrawAll(self, canvas):
        
    #     if self.waitingForInput: return
    #     posDraftMode.drawGrid(self, canvas)

    # def drawGrid(self, canvas):
        
    #     x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.displayedPlayers)))
    #     inc = y1

    #     for i in range(len((self.displayedPlayers))):
    #         canvas.create_rectangle(x0,y0,x1,y1, width = 5)
    #         midX = (x0 + x1)/2
    #         midY = (y0 + y1)/2
    #         canvas.create_text(midX, midY, text = self.displayedPlayers[i]
    #         , font = "STIXVariants 16 bold")

    #         y0 += inc
    #         y1 += inc

                
# class advDraftMode(Mode):
    
#     def appStarted(self):
#         self.waitingForInput = True
#         self.numRosters = int(self.getUserInput("Enter number of teams: "))
#         self.pick = int(self.getUserInput("Enter pick number:")) - 1
#         self.customRoster = self.getUserInput("Choose Custom Roster(y/n)? Default is 1 QB, 2 WR, 2 RB, 1 TE")
#         if 'y' in self.customRoster:
#             self.customQB = int(self.getUserInput("Enter QBs in Roster:"))
#             self.customRB = int(self.getUserInput("Enter RBs in Roster:"))
#             self.customWR = int(self.getUserInput("Enter WRs in Roster:"))
#             self.customTE = int(self.getUserInput("Enter TEs in Roster:"))
#             self.AIRosters = adversarialDraft(self.numRosters, Player.allPlayers,
#              {"qb": self.customQB, "wr": self.customWR, "rb": self.customRB, "te":self.customTE })
#         else:
#             self.AIRosters = adversarialDraft(self.numRosters, Player.allPlayers)
#         self.displayedPlayers = []
        
#         for pos in self.AIRosters[self.pick]:
#             for player in self.AIRosters[self.pick][pos]:
#                 self.displayedPlayers.append(player)
   
#         self.waitingForInput = False

#     def redrawAll(self, canvas):
#         if self.waitingForInput: return
#         advDraftMode.drawGrid(self, canvas)
    
#     def drawGrid(self, canvas):
        
#         x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.displayedPlayers)))
#         inc = y1

#         for i in range(len((self.displayedPlayers))):
#             canvas.create_rectangle(x0,y0,x1,y1, width = 5)
#             midX = (x0 + x1)/2
#             midY = (y0 + y1)/2
#             canvas.create_text(midX, midY, text = self.displayedPlayers[i]
#             , font = "STIXVariants 16 bold")

#             y0 += inc
#             y1 += inc

# class minimaxDraftMode(Mode):
    
#     def appStarted(self):
#         self.waitingForInput = True
#         self.numRosters = 2
#         self.pick = int(self.getUserInput("Enter pick number(1 or 2):")) - 1
#         self.customRoster = self.getUserInput("Choose Custom Roster(y/n)? Default is 1 QB, 2 WR, 2 RB, 1 TE")
#         if 'y' in self.customRoster:
#             self.customQB = int(self.getUserInput("Enter QBs in Roster:"))
#             self.customRB = int(self.getUserInput("Enter RBs in Roster:"))
#             self.customWR = int(self.getUserInput("Enter WRs in Roster:"))
#             self.customTE = int(self.getUserInput("Enter TEs in Roster:"))
#             self.AIRosters = positionalDraft(self.numRosters, Player.allPlayers,
#              {"qb": self.customQB, "wr": self.customWR, "rb": self.customRB, "te":self.customTE })
#         else:
#             self.AIRosters = positionalDraft(self.numRosters, Player.allPlayers)
#         self.displayedPlayers = []
        
#         for pos in self.AIRosters[self.pick]:
#             for player in self.AIRosters[self.pick][pos]:
#                 self.displayedPlayers.append(player)
   
#         self.waitingForInput = False

#     def redrawAll(self, canvas):
#         if self.waitingForInput: return
#         minimaxDraftMode.drawGrid(self, canvas)
    
#     def drawGrid(self, canvas):
        
#         x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.displayedPlayers)))
#         inc = y1

#         for i in range(len((self.displayedPlayers))):
#             canvas.create_rectangle(x0,y0,x1,y1, width = 5)
#             midX = (x0 + x1)/2
#             midY = (y0 + y1)/2
#             canvas.create_text(midX, midY, text = self.displayedPlayers[i]
#             , font = "STIXVariants 16 bold")

#             y0 += inc
#             y1 += inc


class helpMode(Mode):

    def appStarted(self):
        self.margin = 50
        self.image = self.loadImage('helpmodepic.png')
        self.helpModePageImage = self.scaleImage(self.image, self.width/self.image.size[0])


    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.helpModePageImage))
        # canvas.create_text(self.width/2, self.margin , 
        # text = "Help & Instructions", font = "STIXVariants 26 bold")
        # canvas.create_text(self.width/2, self.margin*2, anchor = "n", 
        # text = '''
        # Description:\n        This tool will help you practice different drafting 
        # strategies for fantasy football. Using four distinct 
        # AI drafting algorithms, you can simulate how your 
        # leaguemates choose players. This tool also offers a 
        # player lookup feature so you can learn more about 
        # specific players.''',
        # font = "STIXVariants 15 bold")
        # canvas.create_text(self.width/2, self.height/2, anchor = "n", 
        # text = '''
        # Instructions:
        # On the next page, you can select any of the four draft
        # algorithms to test. You will be prompted to enter
        # the number of teams in the league, and which position 
        # you'd like to pick at.\n
        # To Start Drafting: Press d
        # To Open Player Lookup: Press lb
        # ''',
        # font = "STIXVariants 15 bold")
        

    def keyPressed(mode, event):
        if event.key == 'd' or event.key == 'D':
            mode.app.setActiveMode(mode.app.selectionMode)
        elif event.key == 'f' or event.key == 'F':
            mode.app.setActiveMode(mode.app.playerLookupMode)
        elif event.key == 'Escape':
            mode.app.setActiveMode(mode.app.splashPageMode)
       
class playerLookupMode(Mode):

    def getRow(self, x, y): # modified version of getCell, only 1 col so just row
        cellHeight = self.height/self.numberOfPlayers
        row = y // cellHeight
        if x >= self.width/2:
            return row
        return None

    def mousePressed(self, event):
        row = (playerLookupMode.getRow(self, event.x, event.y))
        if row != None:
            self.selectedPlayer = self.displayedPlayers[int(row)]
            self.app.alphaSelectedPlayer = self.selectedPlayer
            self.app.setActiveMode(self.app.playerStatsMode)
        
    def redrawAll(self, canvas):
        # canvas.create_text(self.width/8, 0, 
        # text = "Player Lookup",
        # font = "STIXVariants 20 bold", anchor = "nw")

        # canvas.create_text(self.width/8, self.height/10, 
        # text = "Click on a player name\n to view their stats",
        # font = "STIXVariants 14 bold", anchor = "nw")

        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.backgroundImage))

        playerLookupMode.drawGrid(self, canvas)
        playerLookupMode.drawSearchBar(self, canvas)
        interval = 5
        if self.timer % interval == 0:
            playerLookupMode.drawSearchBarIcon(self, canvas)

    def appStarted(self):
        self.numberOfPlayers = 12
        defaultRoster = {"qb": set(), "wr": set(), "rb":set(), "te": set()}
        rosters = [copy.deepcopy(defaultRoster) for i in range(self.numberOfPlayers)]
        self.defaultSuggestions = getSuggestedPlayers(rosters[0], Player.allPlayers, 
        rosters)
        self.selectedPlayer = None
        self.searchBarMode = True
        self.showSearchBar = False
        self.searchContents = ""
        self.sbm = min(self.width,self.height)/30 # sbm means search bar margin
        self.searchBarDim = [self.width/4 - self.sbm*4, self.height/2 -self.sbm, self.width/4 + self.sbm*4, self.height/2 + self.sbm ]
        self.searchOutput = None
        self.searchBarIconDim  =  [self.searchBarDim[0], self.searchBarDim[1], self.searchBarDim[0] + self.searchBarDim[2] * 0.01, self.searchBarDim[3]]
        self.origIconDim = copy.deepcopy(self.searchBarIconDim)
        self.displayedPlayers = self.defaultSuggestions
        self.originalImage = self.loadImage('playerfinder.png')
        self.backgroundImage = self.scaleImage(self.originalImage, self.width/self.originalImage.size[0])
        self.timer = 0

    def timerFired(self):
        self.searchContents.strip().lower()
        self.timer += 1
        self.displayedPlayers = []
        
        if self.searchContents == "":
            self.displayedPlayers = self.defaultSuggestions
            return

        i = 0
        # len(self.displayedPlayers) < self.numberOfPlayers 
        Player.allPlayers = copy.deepcopy(self.app.playerListCopy)
        while (i < len(Player.allPlayers)):
            if self.searchContents in Player.allPlayers[i].name.lower():
                self.displayedPlayers.append(Player.allPlayers[i])
            i += 1
        
    def drawSearchBarIcon(self, canvas):
        x0, y0, x1, y1 = self.searchBarIconDim
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
 
    def drawGrid(self, canvas):
        
        x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.defaultSuggestions)))
        inc = y1

        for i in range(len((self.displayedPlayers))):
            canvas.create_rectangle(x0,y0,x1,y1, width = 5, outline = 'White')
            midX = (x0 + x1)/2
            midY = (y0 + y1)/2
            canvas.create_text(midX, midY, text = self.displayedPlayers[i],
            font = "STIXVariants 16 bold", fill = 'White')

            y0 += inc
            y1 += inc

    def drawSearchBar(self, canvas):
        x0, y0, x1, y1 = self.searchBarDim
        canvas.create_rectangle(x0,y0,x1,y1, fill = "lightgreen")
        midX = (x0 + x1)/2
        midY = (y0 + y1)/2
        canvas.create_text(x0, midY, text = self.searchContents,
        font = "STIXVariants 14", anchor = "w")
       
    def keyPressed(self, event):
        if event.key == 'Escape':
            self.app.setActiveMode(self.app.helpMode)
        if self.searchBarMode:
            if event.key == "Backspace":
                self.searchContents = self.searchContents[:-1]
            elif event.key == "Space":
                self.searchContents += " "
            elif event.key in string.ascii_letters:
                self.searchContents += event.key

        iconInc = 8.45*(min(self.width, self.height)/600) # hardcoded to 600 x 600 window, increment for the icon
        self.searchBarIconDim[0] = self.origIconDim[0] + iconInc*len(self.searchContents)
        self.searchBarIconDim[2] = self.origIconDim[2] + iconInc*len(self.searchContents)
       
class playerStatsMode(Mode):

    def appStarted(self):
        self.player = self.app.alphaSelectedPlayer
        self.marginFactor = 8 
        self.margin = self.width/self.marginFactor
        self.attributeValues = []
        self.displayedAttributes = []
        self.attributeValues, self.displayedAttributes = playerStatsMode.initAttributes(self, self.player)
        self.originalImage = self.loadImage('playerStats.png')
        self.backgroundImage = self.scaleImage(self.originalImage, self.width/self.originalImage.size[0])

    def resetAttributes(self):
        self.player = self.app.alphaSelectedPlayer
        self.marginFactor = 8 
        self.margin = self.width/self.marginFactor
        self.attributeValues = []
        self.displayedAttributes = []
        self.attributeValues, self.displayedAttributes = playerStatsMode.initAttributes(self, self.player)

    # attributes based on each pos
    def initAttributes(self, player):
        posi = player.pos.strip().lower()
        attributeValues = []
        displayedAttributes = []

        if posi == 'rb':
            attributeValues = [player.name, player.pos, player.age,
            player.rushYds, player.rushAtt, 
            player.ya, player.rushTds, player.fScore]
            displayedAttributes = ['Name', 'Position', 'Age', 'Rush Yards', 'Attempts', 'Yards per Attempt',
            'Rushing TDs', 'fScore']

        elif posi == 'qb':
            attributeValues = [player.name,player.pos, player.age, player.cmp, player.att, player.passYds,
            player.passTds, player.ints, player.fScore]
            displayedAttributes = ['Name','Position', 'Age', 'Completions', 'Attempts', 'Pass Yards',
            'Passing TDs', 'Interceptions', 'fScore']

        elif posi == 'wr' or posi == 'te':
            attributeValues = [player.name, player.pos, player.age, player.tgts, player.rec, player.recYds, player.yr,
            player.recTds, player.fScore]
            displayedAttributes = ['Name','Position', 'Age', 'Targets', 'Receptions', 'Receiving yards',
            'Yards per Reception', 'Receiving TDs', 'fScore']

        return attributeValues, displayedAttributes

    def redrawAll(self, canvas):
        
        playerStatsMode.resetAttributes(self) 
        canvas.create_image(self.width/2, self.height/2, image = ImageTk.PhotoImage(self.backgroundImage))
        playerStatsMode.drawGrid(self, canvas)
        # canvas.create_text(self.width/4, self.height/2, 
        # text = "Press Esc to return\nto the player lookup screen",
        # font = "STIXVariants 13 bold")
    
    def drawGrid(self, canvas):
        
        x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.attributeValues)))
        inc = y1

        for i in range(len((self.attributeValues))):
            canvas.create_rectangle(x0,y0,x1,y1, width = 5, outline = 'White')
            midX = (x0 + x1)/2
            midY = (y0 + y1)/2
            canvas.create_text(midX, midY,
             text = f"{self.displayedAttributes[i]}: {(self.attributeValues[i])}"
            , font = "STIXVariants 16 bold", fill = 'White')

            y0 += inc
            y1 += inc
    
    def keyPressed(self, event):
        if event.key == 'Escape':
            self.app.setActiveMode(self.app.playerLookupMode)
            

class draftResultsMode(Mode):

    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setSize(width = 600, height = 600)
            self.app.setPosition(0,0)
            self.app._root.resizable(False, False)
            self.app.setActiveMode(self.app.draftMode)
    
    def initAttributes(self):
        self.waitingForInput = True
        self.numRosters = self.app.numTeams 
        self.pick = self.app.pick
        self.draftType = self.app.draftType
        self.displayedPlayers = [[None for i in range(6)] for i in range(self.numRosters)]

        if self.draftType == 0:
            self.rosters = autoDraft(self.numRosters, Player.allPlayers)
            self.displayedPlayers = copy.deepcopy(self.rosters)
        else:
            if self.draftType == 1:
                self.rosters = positionalDraft(self.numRosters, Player.allPlayers)
            elif self.draftType == 2:
                self.rosters = adversarialDraft(self.numRosters, Player.allPlayers, self.pick)
            elif self.draftType == 3:
                self.rosters = minimaxDraft(self.numRosters, Player.allPlayers, True)
            
            
            for i in range(len(self.rosters)):
                rospos = 0
                for pos in self.rosters[i]:
                    for player in self.rosters[i][pos]:
                        self.displayedPlayers[i][rospos] = player
                        rospos += 1
                                  
        self.cols = len(self.displayedPlayers) 
        self.disRows = len(self.displayedPlayers[0])
        self.rows = self.disRows + 1
        self.waitingForInput = False
        self.timer = 0
        self.fontSize = 10/(self.cols/8)
        Player.allPlayers = copy.deepcopy(self.app.playerListCopy)

    def appStarted(self):
        draftResultsMode.initAttributes(self)
        self.timer = 10

    

    def getCellBounds(self, row, col):
        cellHeight = self.height/self.rows
        cellWidth = self.width/self.cols
        x0 = cellWidth * col
        y0 = cellHeight * row
        x1 = x0 + cellWidth
        y1 = y0 + cellHeight

        return(x0, y0, x1, y1)

    def redrawAll(self, canvas):
        if not self.waitingForInput:
            draftResultsMode.drawGrid(self, canvas)
    
    def timerFired(self):
        
        if self.app.draftChanged:
            draftResultsMode.initAttributes(self)
            self.app.draftChanged = False
        
    
    def drawGrid(self, canvas):
        
        for col in range(self.cols):
            x0, y0, x1, y1 = draftResultsMode.getCellBounds(self, 0, col)
            midX = (x0 + x1)/2
            midY = (y0 + y1)/2
            if col != self.pick - 1:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "White")
                canvas.create_text(midX, midY, text = f"Team {col + 1}",
                font = f'STIXVariants {int(self.fontSize)} bold')
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "lightgreen")
                canvas.create_text(midX, midY, text = f"Your Team",
                font = f"STIXVariants {int(self.fontSize)} bold")
        
        # col, board of player list, 
        currRow = 1
        for col in range(self.cols):
            currRow = 1
            for row in range(self.disRows):
                x0, y0, x1, y1 = draftResultsMode.getCellBounds(self, currRow, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = "White")
                midX = (x0 + x1)/2
                midY = (y0 + y1)/2
                currRow += 1
                canvas.create_text(midX, midY, text = self.displayedPlayers[col][row],
                font = f"STIXVariants {int(self.fontSize)} bold")
            
        # x0,y0,x1,y1 = self.width/2,0,self.width,self.height/((len(self.displayedPlayers)))
        # inc = y1

        # for i in range(len((self.displayedPlayers))):
        #     canvas.create_rectangle(x0,y0,x1,y1, width = 5)
        #     midX = (x0 + x1)/2
        #     midY = (y0 + y1)/2
        #     canvas.create_text(midX, midY, text = self.displayedPlayers[i]
        #     , font = "STIXVariants 16 bold")

            # y0 += inc
            # y1 += inc


class FantasyFootballDraftPracticer(ModalApp):
    def appStarted(self):
        self.splashPageMode = splashPageMode()
        self.helpMode = helpMode()
        self.selectionMode = selectionMode()
        self.playerLookupMode = playerLookupMode()
        self.draftMode = draftMode()
        self.playerStatsMode = playerStatsMode()
        self.draftResultsMode = draftResultsMode()
        self.setActiveMode(self.splashPageMode)
        self.draftType = None
        self.alphaSelectedPlayer = None
        self.timerDelay = 200
        self.draftChanged = False
        self.playerListCopy = copy.deepcopy(Player.allPlayers)

   
def main():
    FantasyFootballDraftPracticer(width = 600, height = 600, 
    title = "Fantasy Football Draft Practicer")

if __name__ == '__main__':
    main()
