```promela
int num = 5;
int result = 0;

proctype factorial(int n) {
  int i = 0;
  int temp_result = 1;

  if
  :: n == 0 ->
    result = 1;
    printf("Factorial of 0 is 1
")
  :: else ->
    i = 1;
    do
    :: i <= n ->
      temp_result = temp_result * i;
      i++;
    :: else ->
      break;
    od;
    result = temp_result;
    printf("Factorial of %d is %d
", n, result)
  fi;
}

init {
  run factorial(num);
}
```