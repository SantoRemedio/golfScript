# Operator .
# args: 1
# Duplicate top of divisor.
#
# 1 2 3. -> 1 2 3 3

def gs_dup(stack):
    stack.append(stack[-1])
