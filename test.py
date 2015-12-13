import re
valid = re.compile("^[A-F0-9]{16}$|^[A-F0-9]{32}$|^[A-F0-9]{64}$")
result = valid.match(input())
print(result)