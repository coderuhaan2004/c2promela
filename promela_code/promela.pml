```promela
int fib_n = 10;
int fib_a = 0;
int fib_b = 1;
int fib_next;
int fib_i;

init {
  printf("Fibonacci series up to %d terms:
", fib_n);

  fib_i = 0;
  do
  :: fib_i < fib_n ->
    printf("%d ", fib_a);
    fib_next = fib_a + fib_b;
    fib_a = fib_b;
    fib_b = fib_next;
    fib_i = fib_i + 1;
  :: else -> break;
  od;

  printf("
");
}
```