import numpy as np
from func import *
import copy


def calc_dimens(mu):
    if mu == list(L):
        return 1
    if np.dot(L + ro, L + ro) == np.dot(mu + ro, mu + ro):
        return 0
    s = 0
    for p in positives:
        i = 1
        while np.dot(mu + i*p, mu + i*p) <= np.dot(L, L):
            for j in range(len(weights)):
                if list(mu + i*p) in weights[j]:
                    if dimensions[j] == -1:
                        return -1
                    s += 2* dimensions[j] * np.dot(mu+i*p, p)
            i += 1
    return s / (np.dot(L + ro, L + ro) - np.dot(mu + ro, mu + ro))


def Is_weight(w):
    for i in range(len(weights)):
        for v in weights[i]:
            if list(w) == v and dimensions[i] != 0:
                return True
    return False

def check_onedim(w):
    for i in range(len(weights)):
        if list(w) in weights[i]:
            if dimensions[i] == 1:
                return True
            else:
                return False    


def gen_path(l, w):  ## generate all paths from l to w
    if list(l - w) == [0, 0, 0, 0]:
        return [""]
    ans = []
    for i in range(4):
        if Is_weight(w+a[i]) and IsPos(l - w - a[i]):
            helper = gen_path(l, w+a[i])
            for p in helper:
                ans += [str(i+1)+p]
    if check_onedim(w):
        return [ans[0]]
    return ans

def action(v, d):
    res = []
    w = copy.deepcopy(L)
    for i in range(len(v) - 1, -1, -1):
        if int(v[i]) == d:
            flag = True
            helper = copy.deepcopy(w)
            for j in range(i - 1, -1, -1):
                helper -= a[int(v[j]) - 1]
                if not Is_weight(helper):
                    flag = False
                    break
            if flag:
                res += [[v[:i]+v[i+1:], prod(w, a[int(v[i])-1])]]
        w -= a[int(v[i]) - 1]
    return res
    
def calc_com(vect, comm):
    res = []
    if len(comm) == 1:
        for v in vect:
            helper = action(v[0], int(comm))
            for h in helper:
                h[1] *= v[1]
                if h[1] != 0:
                    res.append(h)
        flag = True
        while flag:
            flag = False
            for i in range(len(res)):
                if flag:
                    break
                for j in range(i+1, len(res)):
                    if res[i][0] == res[j][0]:
                        flag = True
                        res[i][1] += res[j][1]
                        res.pop(j)
                        break
        return res  
    c = int(comm[-1])
    for v in vect:
        helper = action(v[0], c)
        for h in helper:
            h[1] *= v[1]
            if h[1] != 0:
                res.append(h)
    res = calc_com(res, comm[:-1])
    helper = calc_com(vect, comm[:-1])
    for h in helper:
        helper2 = action(h[0], c)
        for h2 in helper2:
            h2[1] *= (-1)*h[1]
            if h2[1] != 0:
                res.append(h2)
    flag = True
    while flag:
        flag = False
        for i in range(len(res)):
            if flag:
                break
            for j in range(i+1, len(res)):
                if res[i][0] == res[j][0]:
                    flag = True
                    res[i][1] += res[j][1]
                    res.pop(j)
                    break
    return res  
        
def reflect(vect, c):
    res = []
    if len(vect) == 0:
        return []
    for v in vect:
        if v[0] == '':
            res += [[gen_path(L, L - prod(L, a[int(c) - 1])*a[int(c) - 1])[0], v[1]]]
        else:
            direct = v[0][0]
            helper = reflect([[v[0][1:], v[1]]], c)
            w = np.array([0, 0, 0, 0], float)
            if helper:
                for h in helper[0][0]:
                    w += a[int(h) - 1]
            w = L - w            
            if direct == c:
                res += calc_com(helper, c)
            elif abs(int(direct) - int(c)) > 1:
                for h in helper:
                    res += [[direct + h[0], h[1]]]
            elif direct == '3' and c == '2':
                if Is_weight(w - a[1]):
                    if Is_weight(w - a[1] - a[2]):
                        for h in helper:
                            res += [['232' + h[0], h[1]*2]]
                    if Is_weight(w - a[1] - a[1]):
                        for h in helper:
                            res += [['322' + h[0], -1*h[1]]]
                if Is_weight(w - a[2]) and Is_weight(w - a[2] - a[1]):
                    for h in helper:
                        res += [['223' + h[0], -1*h[1]]]
            else:
                if Is_weight(w - a[int(c) - 1]):
                    for h in helper:
                        res += [[direct + c + h[0], h[1]]]
                if Is_weight(w - a[int(direct) - 1]):
                    for h in helper:
                        res += [[c + direct + h[0], -1*h[1]]]
    flag = True
    while flag:
        flag = False
        for i in range(len(res)):
            if flag:
                break
            for j in range(i+1, len(res)):
                if res[i][0] == res[j][0]:
                    flag = True
                    res[i][1] += res[j][1]
                    res.pop(j)
                    break
    return res      
                            
                
    
    
    
    
    


x1, x2, x3, x4 = map(float, input().split())

L = (x1*e[0] + x2*e[1] + x3*e[2] + x4*e[3]) ## higher weight lambda
LEN = np.dot(L, L)



weights = [gen_orbit(L)]


start = 0

finish = 1

while True:
    extend = False
    for i in range(start, finish):
        if extend:
            break        
        for w in weights[i]:
            if extend:
                break            
            for j in range(4):
                isFound = False
                if np.dot(w-a[j], w-a[j]) > LEN:
                    continue
                for o in weights:
                    if list(w - a[j]) in o:
                        isFound = True
                        break
                if not isFound:
                    weights.append(gen_orbit(w - a[j]))
                    extend = True
                    finish += 1
                    break
        if not extend:
            start += 1
    if not extend:
        break

dimensions = [-1] * len(weights)

while -1 in dimensions:
    for i in range(len(weights)):
        if dimensions[i] == -1:
            dimensions[i] = calc_dimens(weights[i][0])

result = []

for i in range(len(weights)):
    if dimensions[i] != 0:
        result += [[weights[i][0], len(weights[i]), dimensions[i]]]
result.sort(key = lambda x: x[0], reverse = True)
for r in result:
    print(r[0], r[1], r[2])

print()
print()
ans = 0                
for r in result:
    ans += r[1]*r[2]
print(ans)
print()        
print()
com = int(input())

bufer = []

while com != 0:
    if com == 1: ## generating all paths to the weight
        x1, x2, x3, x4 = map(float, input().split())
        w = x1*e[0] + x2*e[1] + x3*e[2] + x4*e[3]
        if Is_weight(w):
            print(gen_path(L, w))
            print()
        else:
            print("It is not a weight")
    if com == 2:
        v = input()
        direction = int(input())
        print(action(v, direction))
        print()
    if com == 3:
        v = input()
        for i in range(1, 5):
            print("e"+str(i)+": ", action(v, i))
        print()
    if com == 4:
        n = int(input())
        vect = []
        for i in range(n):
            v, d = input().split()
            vect += [[v, float(d)]]
        c = input()
        print(calc_com(vect, c))
    if com == 5:
        n = int(input())
        vect = []
        for i in range(n):
            v, d = input().split()
            vect += [[v, float(d)]]
        c = input()
        bufer = reflect(vect, c)
        print(bufer)
        print()
    if com == 6:
        x1, x2, x3, x4 = map(float, input().split())
        w = x1*e[0] + x2*e[1] + x3*e[2] + x4*e[3]
        d = int(input()) - 1
        print(w - prod(w, a[d])*a[d])
    if com == 7:
        c = input()
        print(calc_com(bufer, c))
    com = int(input())