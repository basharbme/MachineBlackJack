from file_interface import File
from game import Game
import multiprocessing as mp

def generate_nodes(manager):
    files = manager.dict()
    for i in range(1, 23):
        for j in range(1, 23):
            file_name = 'data/'+str(i)+"_"+str(j)+".txt"
            file = open(file_name, 'w')
            file.write('10')
            file.close()
            files[file_name] = File(file_name, manager)
    file = open('data/root.txt', 'w')
    file.write('')
    file.close()
    files['data/root.txt'] = File('data/root.txt', manager)
    return files

def play(files, lock):
    game = Game(files, lock)
    while not game.next_round():
        pass
    res = game.finish_game()
    game.learn(str(int(res)))

if __name__ == '__main__':
    manager = mp.Manager()
    files = generate_nodes(manager)
    lock = mp.Lock()
    jobs = []
    for i in range(2):
        for j in range(4):
            jobs.append(mp.Process(target=play, args=(files,lock,)))
            jobs[j].start()
        for j in range(len(jobs)):
            jobs[j].join()
        print("done "+str(i))
        jobs.clear()