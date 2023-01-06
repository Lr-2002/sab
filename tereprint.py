from collections import deque
# ?dq = deque()
li = [1,2,3,4]
dq =deque(li)
ll = li[:2]
print(dq)
dq.popleft()
print(dq, li ,ll)
ll.pop(0)
print(dq, li ,ll)

