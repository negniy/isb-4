import hashlib
import multiprocessing as mp
from tqdm import tqdm

SETTING = {
    'hash': '754a917a9c82f5247412006a5abe1c0eb76e1007',
    'begin_digits': '529460', 
    'last_digits': '0758',
}

def check_hash(x):
    all_n = '529460'+str(x)+'0758' ## 529460940360758
    hash = hashlib.sha1(all_n.encode()).hexdigest()
    if (hash == '754a917a9c82f5247412006a5abe1c0eb76e1007'):
        return True
    return False


def sample_function(x):
        return x if check_hash(x) == True else False


if __name__ == "__main__":
    print('begin')
    
    with mp.Pool(36) as p:
        for result in p.map(sample_function, tqdm(range(99999, 10000000))):
            if result:
                print(f'we have found {result} and have terminated pool')
                p.terminate()
                break
    print('end')