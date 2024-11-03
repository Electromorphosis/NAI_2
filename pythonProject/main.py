'''
#Wymagane biblioteki: [ numpy,pygame,matplotlib,scikit-fuzzy,networkx,scipy]
'''
import gameplay.game as game
import ai_system.fuzzy as fuzzy

if __name__ == "__main__":
    game.main(1000,1000, fuzzy)
