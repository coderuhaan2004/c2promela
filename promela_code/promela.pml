```promela
int n_global = 10;
int a_global = 0;
int b_global = 1;
int next_global;

proctype fibonacci() {
  int i_local = 0;

  printf("Fibonacci series up to %d terms:
", n_global);

  do
  :: (i_local < n_global) ->
    printf("%d ", a_global);
    next_global = a_global + b_global;
    a_global = b_global;
    b_global = next_global;
    i_local = i_local + 1;
  :: (i_local >= n_global) ->
    break;
  od;

  printf("
");
}

init {
  run fibonacci();
}
```