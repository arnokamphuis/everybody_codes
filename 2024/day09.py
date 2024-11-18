import sys

day = 9

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [int(line.strip()) for line in file]

if part == 1:
    stamps = [10, 5, 3, 1]

    count = 0
    for r in data:
        rest = r
        required = []
        for index in range(len(stamps)):
            required.append( rest // stamps[index] )
            rest = rest % stamps[index]
        print(required)
        count += sum(required)
    print(count)
    
elif part >= 2:
    stamps = [30, 25, 24, 20, 16, 15, 10, 5, 3, 1] if part == 2 else [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]

    DP = {}
    def find_required_beetles(r):
        if r < 0:
            return 1e99
        if r == 0:
            return 0
        if r in DP:
            return DP[r]
        
        required = 1e99
        
        for stamp in stamps:
            rb = 1 + find_required_beetles(r-stamp)
            required = min(required, rb)
        DP[r] = required
        return required

    if part == 2:
        count = 0
        for r in data:
            count += find_required_beetles(r)
        print(count)    
    else:
        stamps_needed = [0]
        for sparkles in range(1, 10**7):
            if sparkles % 100000 == 0:
                print(sparkles // 100000,end=" ")
            min_stamps = 1e99
            for stamp in stamps:
                if (sparkles - stamp) >= 0:
                    min_stamps = min(min_stamps, 1 + stamps_needed[sparkles-stamp])
            stamps_needed.append(min_stamps)
                                
        count = 0
        for r in data:
            hr = r//2
            min_needed = 1e99
            for item in range(hr-200, hr+200):
                rest = r - item                
                if  abs(item-rest) <= 100:
                    total_needed = stamps_needed[item] + stamps_needed[r - item]
                    if min_needed > total_needed:
                        min_needed = total_needed
            count += min_needed
        print(count)