#!/usr/bin/python

prev_size = 4
align_length = 2 * prev_size

def get_malloc_chunk_size(size):
    data_size = 0
    if size < align_length + prev_size:  # < 2*4+4
        data_size = align_length
    else:
        if (size  - (size / align_length) * align_length) > prev_size:
            data_size = align_length * (1 + size / align_length)
        else:
            data_size = align_length * (size / align_length)

    return 2 * prev_size + data_size # chunk_header  + data_size

def check_addr(addr):
    if addr & 0x8 == 0x8:
        return True
    else:
        return False

if __name__ == '__main__':
    addr = 8

    for i in xrange(6,13,1): # 6 7 8 9 10 11 12
        
        print pow(2,i), ' <= size < ', pow(2,i+1)
        
        chunk_size = get_malloc_chunk_size(pow(2,i))
        addr = chunk_size + addr
        if check_addr(addr):
            print '  Correct, input :' ,pow(2,i)
            # print 'Size: ', pow(2,i)
        else:
            print '  failed, input :', pow(2,i)+8
            addr += 8
            # print '+8 Now addr:', addr
    