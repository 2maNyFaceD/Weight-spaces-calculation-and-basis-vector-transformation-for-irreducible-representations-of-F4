import numpy as np
import copy


def prod(a, b):
    return (2 * np.dot(a, b))/np.dot(b, b)


def gen_orbit(w):
    orbit = [list(w)]
    while True:
        flag = True
        for a in orbit:
            for p in positives:
                v = a - prod(a, p)*p
                if list(v) not in orbit:
                    orbit.append(list(v))
                    flag = False
                    if IsDom(v):
                        orbit[0], orbit[-1] = orbit[-1], orbit[0]
        if flag:
            break
    return orbit
            
            
            
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
            if w == v and dimensions[i] != 0:
                return True
    return False

            
def IsPos(w):
    if w[0] < 0:
        return False
    if w[0] + w[1] + w[2] + w[3] < 0:
        return False
    if w[0] + w[1] + w[2] < 0:
        return False
    if w[0] + w[1] < 0:
        return False
    return True

def IsDom(w):
    if w[3] < 0:
        return False
    if w[2] < w[3]:
        return False
    if w[1] < w[2]:
        return False
    if w[0] < w[1]:
        return False
    return True



a = [np.array([1, -1, 0, 0]), np.array([0, 0, 0, 1]), np.array([0, 0, 1, -1]), np.array([0, 1, -1, 0])]

e = [np.array([1, 0, 0, 0]), np.array([0, 1, 0, 0]), np.array([0, 0, 1, 0]), np.array([0, 0, 0, 1])]

ro = np.array(3.5*e[0] + 2.5*e[1] + 1.5*e[2] + 0.5*e[3])

positives = []
for i in range(4):
    positives += [e[i]]
    for j in range(i+1, 4):
        positives += [e[i] - e[j]]
        positives += [e[i] + e[j]]


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