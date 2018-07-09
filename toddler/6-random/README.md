## TARGET
```
random - 1 pt [writeup] 

Daddy, teach me how to use random value in programming!

ssh random@pwnable.kr -p2222 (pw:guest)
```

## WRITEUP
download:  
```
scp -P 2222 -p  random@pwnable.kr:/home/random/* ./
```
程序输入用scanf %d 读取一个signed int和rand()异或，如果结果为0xdeadbeef进入system流程。由于rand()调用前没有调用srand()，因此产生的结果可以认为是不变的。   
A ^ B = C ->  A ^ C = B -> B ^ C = A ，任意两个变量异或的值等于第三个值。gdb本地调试，断点设置在rand()后，b *0x400606，可知rand的结果为0x6b8b4567。

```python
>>> 0x6b8b4567^0xdeadbeef
3039230856
```

EXP:
```bash
random@ubuntu:~$ ./random
3039230856
Good!
Mommy, I thought libc random is unpredictable...

```
IDA pseudocode:
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+8h] [rbp-8h]
  int v5; // [rsp+Ch] [rbp-4h]

  v5 = rand();
  v4 = 0;
  __isoc99_scanf(&unk_400760, &v4);
  if ( (v5 ^ v4) == 0xDEADBEEF )
  {
    puts("Good!");
    system("/bin/cat flag");
  }
  else
  {
    puts("Wrong, maybe you should try 2^32 cases.");
  }
  return 0;
}
```

## TIPS
```c
    #include <stdlib.h>
    int rand(void);
    int rand_r(unsigned int *seedp);
    void srand(unsigned int seed);
```
rand() returns a pseudo-random integer. Without srand(),the return value is 1804289383.  
srand() can change the seed which will effect rand(). # default srand(1)  
rand_r()'s seedp argument is used to store state between calls.    

See more at: http://man7.org/linux/man-pages/man3/rand.3.html and glibc also.  
Example:  
```c
#include <stdio.h>
#include <stdlib.h>
void myrand(){
    int a;
    a = rand();
    printf("rand() value # %d\n", a);
}
void mysrand(){
    int a;
    srand(1);
    a = rand();
    printf("srand(1)  rand() value %d\n", a);
}
void main(){
    myrand();
    mysrand();

}
/*
Output:
    rand() value # 1804289383
    srand(1)  rand() value 1804289383
*/
```

## optional: glibc
Here is the source code of rand srand and rand_r() for reference only.Yes, I haven't read it...

```c
// stdlib/rand.c
/* Return a random integer between 0 and RAND_MAX.  */
int
rand (void)
{
  return (int) __random ();
}

// stdlib/random.c
long int
__random (void)
{
  int32_t retval;

  __libc_lock_lock (lock);

  (void) __random_r (&unsafe_state, &retval);

  __libc_lock_unlock (lock);

  return retval;
}

// stdlib/random_r.c
int
__random_r (struct random_data *buf, int32_t *result)
{
  int32_t *state;

  if (buf == NULL || result == NULL)
    goto fail;

  state = buf->state;

  if (buf->rand_type == TYPE_0)
    {
      int32_t val = state[0];
      val = ((state[0] * 1103515245) + 12345) & 0x7fffffff;
      state[0] = val;
      *result = val;
    }
  else
    {
      int32_t *fptr = buf->fptr;
      int32_t *rptr = buf->rptr;
      int32_t *end_ptr = buf->end_ptr;
      int32_t val;

      val = *fptr += *rptr;
      /* Chucking least random bit.  */
      *result = (val >> 1) & 0x7fffffff;
      ++fptr;
      if (fptr >= end_ptr)
	{
	  fptr = state;
	  ++rptr;
	}
      else
	{
	  ++rptr;
	  if (rptr >= end_ptr)
	    rptr = state;
	}
      buf->fptr = fptr;
      buf->rptr = rptr;
    }
  return 0;

 fail:
  __set_errno (EINVAL);
  return -1;
}

```

```c
// stdlib/random.c
void
__srandom (unsigned int x)
{
  __libc_lock_lock (lock);
  (void) __srandom_r (x, &unsafe_state);
  __libc_lock_unlock (lock);
}
// stdlib/random_r.c
/* Initialize the random number generator based on the given seed.  If the
   type is the trivial no-state-information type, just remember the seed.
   Otherwise, initializes state[] based on the given "seed" via a linear
   congruential generator.  Then, the pointers are set to known locations
   that are exactly rand_sep places apart.  Lastly, it cycles the state
   information a given number of times to get rid of any initial dependencies
   introduced by the L.C.R.N.G.  Note that the initialization of randtbl[]
   for default usage relies on values produced by this routine.  */
int
__srandom_r (unsigned int seed, struct random_data *buf)
{
  int type;
  int32_t *state;
  long int i;
  int32_t word;
  int32_t *dst;
  int kc;

  if (buf == NULL)
    goto fail;
  type = buf->rand_type;
  if ((unsigned int) type >= MAX_TYPES)
    goto fail;

  state = buf->state;
  /* We must make sure the seed is not 0.  Take arbitrarily 1 in this case.  */
  if (seed == 0)
    seed = 1;
  state[0] = seed;
  if (type == TYPE_0)
    goto done;

  dst = state;
  word = seed;
  kc = buf->rand_deg;
  for (i = 1; i < kc; ++i)
    {
      /* This does:
	   state[i] = (16807 * state[i - 1]) % 2147483647;
	 but avoids overflowing 31 bits.  */
      long int hi = word / 127773;
      long int lo = word % 127773;
      word = 16807 * lo - 2836 * hi;
      if (word < 0)
	word += 2147483647;
      *++dst = word;
    }

  buf->fptr = &state[buf->rand_sep];
  buf->rptr = &state[0];
  kc *= 10;
  while (--kc >= 0)
    {
      int32_t discard;
      (void) __random_r (buf, &discard);
    }

 done:
  return 0;

 fail:
  return -1;
}

```

```c

// stdlib/random_r.c

/* This algorithm is mentioned in the ISO C standard, here extended
   for 32 bits.  */
int
rand_r (unsigned int *seed)
{
  unsigned int next = *seed;
  int result;

  next *= 1103515245;
  next += 12345;
  result = (unsigned int) (next / 65536) % 2048;

  next *= 1103515245;
  next += 12345;
  result <<= 10;
  result ^= (unsigned int) (next / 65536) % 1024;

  next *= 1103515245;
  next += 12345;
  result <<= 10;
  result ^= (unsigned int) (next / 65536) % 1024;

  *seed = next;

  return result;
}

```