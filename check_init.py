import hashlib
import multiprocessing as mp
from tqdm import tqdm

SETTING = {
    'hash': '4f9cbbc1e5a60f526a58cde1343acd900b3f918f6fdff73eb82b0b87ae7d8e22',
    'begin_digits': ['418831', '448331', '448346', '448369', '485990', '429158', '431336', '465208', '465274', '425154'],
    'last_digits': '5574',
}


def algoritm_luna(number: int) -> bool:
    number = str(number)
    if len(number)!=6: 
        return False
    bin = [4, 4, 6, 6, 7, 4]
    end = [1, 3, 7]
    check = 8
    code = [int(i) for i in number]
    all_number = bin+code+end
    for i, num in enumerate(code):	    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            mul = num*2
            if mul > 9:
                mul -= 9
            all_number[i] = mul
    total_sum = sum(all_number)
    rem = total_sum % 10
    check_sum = 10 - rem if rem != 0 else 0
    return number if check_sum == check else False

def check_hash(x):
    a = list(SETTING['begin_digits'])
    for i in a:
        all_n = str(i) + str(x) +'5574'
        h = all_n.encode()
        hash = hashlib.blake2s(h).hexdigest()
        if hash == '4f9cbbc1e5a60f526a58cde1343acd900b3f918f6fdff73eb82b0b87ae7d8e22':
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