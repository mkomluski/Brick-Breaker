import os

def check_highscore():
    try:
        if os.path.exists("data/highscore.txt"):
            with open("data/highscore.txt", "r") as f:
                return int(f.read())
        else:
            return 0
    except:
        return 0
    
def new_highscore(score):
    with open("data/highscore.txt", "w") as f:
        f.write(str(score))