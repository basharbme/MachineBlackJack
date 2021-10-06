from BlackJack.AI.file_interface import File
from BlackJack.AI.game import Game
from BlackJack.settings import BASE_DIR
import multiprocessing as mp

def generate_nodes(manager):
    files = manager.dict()

    for i in range(1, 23):
        for j in range(1, 23):
            file_name = BASE_DIR.as_posix()+'/BlackJack/AI/data/'+str(i)+"_"+str(j)+".txt"
            files[file_name] = File(file_name, manager)
    
    files[BASE_DIR.as_posix()+'/BlackJack/AI/data/root.txt'] = File(BASE_DIR.as_posix()+'/BlackJack/AI/data/root.txt', manager)
    return files

def play(files, lock):
    game = Game(files, lock)
    while not game.next_round():
        pass
    res = game.finish_game()
    game.learn(str(int(res)))

def machine_learning():
    manager = mp.Manager()
    files = generate_nodes(manager)
    lock = mp.Lock()
    jobs = []
    n = 1000000
    for i in range(n):
        for j in range(4):
            jobs.append(mp.Process(target=play, args=(files,lock,)))
            jobs[j].start()

        for j in range(len(jobs)):
            jobs[j].join()

        print("done "+str(i))
        jobs.clear()
