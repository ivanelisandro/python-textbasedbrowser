from collections import deque

# please don't change the following line
candy_bag = deque(input().split())

for _ in range(int(input())):
    action = input().split()
    if action[0] == 'PUT':
        candy_bag.append(action[1])
    if action[0] == 'TAKE':
        print(candy_bag.pop() if candy_bag else "We are out of candies :(")
