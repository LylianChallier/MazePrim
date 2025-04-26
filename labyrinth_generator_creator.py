# Lylian Challier
# Laura Cadillo

import sys
import random

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm

strategy_choice = 1

class Strategy :
    def __init__(self):
        pass

    def Apply(self):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        print("Do Something")

class Algorithm1(Strategy) :
    
    def Apply(self):
        #super().Apply()
        print("Applying Algorithm1")
        
        # Prim
        #random.seed(15) # pour l'implémentation plus simple
        grid = [[ [i,j] for i in range(13)] for j in range(13)]
        visited = [[ False for i in range(13)] for j in range(13)]
        walls = [[ [True, True, True, True] for i in range(13)] for j in range(13)] # North, South, West, East
        hist = [] # historique des coordonnées de la grille

        # INITIALISATION 
        depart = grid[random.randint(0, 12)][random.randint(0, 12)] # choisit un point de départ aléatoire
        visited[depart[0]][depart[1]] = True # visite le point de départ
        hist.append(depart) # on met le point de départ dans l'historique

        # on parcours le labyrinthe
        while visited != [[ True for i in range(13)] for j in range(13)] :
        #for _ in range(5) : # aide pour implémenter
            

            # on fait une liste de voisins valides non visités et on garde une liste associée à leur directions
            voisins = [] 
            directions = []
            if depart[0] != 0 : # exisitent, s'ils sortent pas du maze
                if visited[depart[0]-1][depart[1]] == False : # si pas déjà visité
                    voisins.append([depart[0]-1,depart[1]]) # puis l'ajoute à la liste 
                    directions.append(0) ## North
            if depart[0] != 12 : 
                if visited[depart[0]+1][depart[1]] == False :
                    voisins.append([depart[0]+1, depart[1]]) 
                    directions.append(1) ## South
            if depart[1] != 0 : 
                if visited[depart[0]][depart[1]-1] == False :
                    voisins.append([depart[0], depart[1]-1]) 
                    directions.append(2) ## West
            if depart[1] != 12 : 
                if visited[depart[0]][depart[1]+1] == False :
                    voisins.append([depart[0], depart[1]+1])
                    directions.append(3) ## East

            # on choisit aléatoirement un voisins non visité s'il y en a et prend sa direction
            cardinal = None
            if len(voisins) >= 1 : 
                choix = random.choice(voisins)
                cardinal = directions[voisins.index(choix)]
            else : choix = hist[hist.index(depart)-1] # sinon on retourne en arrière et prend pas de direction


            # selon le cardinal obtenu à partir de la direction du choix, on enlève des murs
            if cardinal != None : 
                walls[depart[0]][depart[1]][cardinal] = False
                
                if cardinal == 0 or cardinal == 2 : 
                    walls[choix[0]][choix[1]][cardinal+1] = False
                elif cardinal == 1 or cardinal == 3 : 
                    walls[choix[0]][choix[1]][cardinal-1] = False

            # prend notre choix comme prochain point sur lequel effectué la bouche
            depart = choix
            # on actualise visited et hist
            visited[depart[0]][depart[1]] = True # visite le point de départ
            hist.append(depart) # on met le point de départ dans l'historique

        # on fait une sortie à la fin du labyrinthe
        ouverture = False
        k = 2
        while ouverture == False : 
            if depart[0] == 0 : # exisitent, s'ils sortent pas du maze
                walls[depart[0]][depart[1]][0] = False # ouvre Nord
                ouverture = True
            elif depart[0] == 12 : 
                walls[depart[0]][depart[1]][1] = False # ouvre Sud
                ouverture = True
            elif depart[1] == 0 : 
                walls[depart[0]][depart[1]][2] = False # ouvre Ouest
                ouverture = True
            elif depart[1] == 12 : 
                walls[depart[0]][depart[1]][0] = False # ouvre Est
                ouverture = True
            else : 
                depart = hist[-k]
                k += 1 

        return walls


class Algorithm2(Strategy) :

    def Apply(self):
        #super().Apply()
        print("Applying Algorithm2")

class Generator() :
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        return self.strategy.Apply()
        

class Creator() :
    def __init__(self):

        pass

    def PrintLabyrinth(self, maze):
        #print(maze)

        with open(f"labyrinth_algo1.scad", "w") as f : 
            f.write(f"// Labyrinth generated for openscad\n")
            f.write(f"// IFT2125 - H24\n")
            f.write(f"// Authors : Lylian Challier & Laura Cadillo\n")
            f.write("difference(){\nunion(){\n")
            f.write("// base plate\ntranslate([-0.5,-0.5,-1]){\ncube([131,131,1], center=false);\n}\n")
            
            for j, row in enumerate(maze) : 
                for i, cell in enumerate(row) : 
                    for k, wall in enumerate(cell) : 
                        if wall == True :
                            if k == 0 : 
                                f.write(f"translate([ {(cell_size)*i+5}, {(cell_size)*j}, 5.0])")
                            if k == 1 : 
                                f.write(f"translate([ {(cell_size)*i+5}, {(cell_size)*j+10}, 5.0])")
                            if k == 2 :  
                                f.write(f"translate([ {(cell_size)*i}, {(cell_size)*j+5}, 5.0])")
                                f.write("{ \n")
                                f.write(f"rotate([0, 0, 90])")
                            if k == 3 :
                                f.write(f"translate([ {(cell_size)*i+10}, {(cell_size)*j+5}, 5.0])")
                                f.write("{ \n")
                                f.write(f"rotate([0, 0, 90])")
                            
                            f.write("{ \n")
                            f.write(f"cube([{cell_size+wall_thickness}, {wall_thickness}, {wall_height}], center=true);")
                            if k == 2 or k==3 : 
                                f.write("\n}") 
                            f.write(" \n} \n")
                        
            #f.write("}\n}\n")
            f.write(f"// logo\n")
            f.write("translate([1,-0.2,1]){\n")
            f.write("rotate([90,0,0]){\n")
            f.write('linear_extrude(1) text("IFT2125 LC", size=7.0);\n')
            f.write("}\n}\n}\n}\n")


# main call
def main():
    global strategy_choice
    args = sys.argv[:]
    if len(args) >= 2 :
        strategy_choice = int(args[1])

    # Generator
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else :
        print("error strategy choice")
    maze = my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth(maze)


if __name__ == "__main__":
    main()
