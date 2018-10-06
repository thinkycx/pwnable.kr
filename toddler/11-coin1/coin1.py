from pwn import *
import re

# context.log_level ='debug'

def binarySearch(left, right):
    middle = int(math.floor( (left+right) / 2.0 ) )
    payload = ' '.join([ str(i) for i in range(left, middle+1 ) ] )
    io.sendline(payload)
    result = io.recvline()
    if 'Correct!' not in result:
	result = int(result)
    else:
	print 'Correct!'
	return
    # print (middle-left + 1)
    if result == 10*(middle -left + 1):
        binarySearch(middle+1, right)
    else:
        binarySearch(left, middle)


def solve(i):
    data = io.recvline()
    log.info("Problem %d : %s" % (i, data) )

    searchObj = re.search("N=(\d*) C=(\d*)", data)
    numberN = int(searchObj.group(1))
    numberC = int(searchObj.group(2))
    if pow(2,numberC) < numberN:
        log.err("cannot solve!")
        exit()

    # print 'start to solve'
    binarySearch(0, numberN-1)

if __name__ == '__main__':
    io = remote('0.0.0.0','9007')
    print io.recv()
    sleep(4)

    for i in range(101):
	if i == 100:
            context.log_level='debug'
        solve(i)
