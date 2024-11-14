import sys

day = 2

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

words = data[0].split(':')[1].split(',')

if part == 1:

    line = data[2].split(' ')
    print('Part {0}: {1}'.format(part, sum(list(map(lambda word: len(list(filter(lambda w: w in word, words))), line)))))

elif part == 2:

    words = words + list(map(lambda w: w[::-1], words))
    lines = data[2:]
    res = 0
    for line in lines:
        for word in line.split(' '):
            counter = list('#'*len(word))
            for runic in words:
                if runic in word:
                    indices = [i for i in range(len(word)) if word.startswith(runic, i)]
                    for i in indices:
                        counter[i:i+len(runic)] = list('1'*len(runic))
            count = len(list(filter(lambda x: x != '#', counter)))
            res = res + count
    print('Part {0}: {1}'.format(part, res))
    
else:
    
    words = words + list(map(lambda w: w[::-1], words))
    active = []
    for col in range(len(data)-2):
        active.append([False]*len(data[2]))

    lines = [list(line) for line in data[2:]]
    res = 0
    
    for t in range(2):
        for row, word in enumerate(lines):
            for runic in words:
                lw = len(word)
                if t == 1:
                    lw = lw - len(runic) + 1
                for col in range(lw):
                    if all([ word[(col+j)%len(word)]==r for j, r in enumerate(runic) ]):
                        for j in range(len(runic)):
                            if t == 0:
                                active[row][(col+j)%len(word)] = True
                            else:
                                active[(col+j)%len(word)][row] = True
        lines = list(map(list, zip(*lines)))
    res = len(list(filter(lambda x: x,[item for row in active for item in row])))
    print('Part {0}: {1}'.format(part, res))
