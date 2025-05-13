```promela
typedef Node {
  int value;
  byte next;
}

#define MAX_NODES 5
#define NULL 255

Node nodes[MAX_NODES];
bool used[MAX_NODES];
byte head = NULL;
byte tail = NULL;

inline my_malloc(ret) {
  byte i = 0;
  do
  :: (i < MAX_NODES) ->
      if
      :: !used[i] ->
          used[i] = true;
          ret = i;
          break
      :: else -> i++
      fi
  :: else -> ret = NULL; break
  od
}

inline my_free(idx) {
  used[idx] = false;
}

proctype test(byte tmp) {
  nodes[tmp].next = NULL;
  if
  :: tail == NULL ->
    head = tmp;
    tail = tmp;
  :: else ->
    nodes[tail].next = tmp;
    tail = tmp;
  fi;
}

proctype print_list() {
  byte current = head;
  printf("Linked List: ");
  do
  :: (current != NULL) ->
    printf("%d -> ", nodes[current].value);
    current = nodes[current].next;
  :: (current == NULL) -> break;
  od;
  printf("NULL");
}

init {
  byte new_node;
  byte i = 1;

  do
  :: (i <= 3) ->
    my_malloc(new_node);
    if
    :: new_node != NULL ->
      nodes[new_node].value = i;
      run test(new_node);
    :: else ->
      printf("Memory allocation failed for node %d", i);
    fi;
    i++;
  :: else -> break;
  od;

  run print_list();

  byte current = head;
  byte next;

  do
  :: (current != NULL) ->
    next = nodes[current].next;
    my_free(current);
    current = next;
  :: else -> break;
  od;

  printf("Memory freed");
}
```