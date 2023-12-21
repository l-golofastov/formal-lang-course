## Язык запросов к графам

### Описание абстрактного синтаксиса языка

```
prog = List<stmt>
stmt =
    bind of var * expr
  | print of expr
val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges
expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход
lambda = Lambda of List<var> * expr
```

### Конкретный синтаксис
```
prog --> (stmt EOL)*
stmt -->
    var '=' expr
  | 'print' expr
var --> initial_letter string
initial_letter --> ID_CHAR
string --> (initial_letter | '/' | '.' | INT)*
expr -->
    L_PARENTHESIS expr R_PARENTHESIS
  | var
  | val
  | map
  | filter
  | intersect
  | concat
  | union
  | star
val -->
    L_PARENTHESIS val R_PARENTHESIS
  | QUOTE string QUOTE
  | INT
  | BOOL
  | graph
  | labels
  | vertices
  | edges
graph -->
    'set_start' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
  | 'set_final' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
  | 'add_start' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
  | 'add_final' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
  | 'load_graph' L_PARENTHESIS path R_PARENTHESIS
  | var
path --> QUOTE string QUOTE | var
vertices -->
    'get_start' L_PARENTHESIS graph R_PARENTHESIS
  | 'get_final' L_PARENTHESIS graph R_PARENTHESIS
  | 'get_reachable' L_PARENTHESIS graph R_PARENTHESIS
  | 'get_vertices' L_PARENTHESIS graph R_PARENTHESIS
  | set
  | var
labels --> 'get_labels' L_PARENTHESIS graph R_PARENTHESIS | set
edges --> 'get_edges' L_PARENTHESIS graph R_PARENTHESIS | set
set --> L_BRACE expr (COMMA expr)* R_BRACE
  | 'set()'
  | L_BRACE ( L_PARENTHESIS INT COMMA (val | var) COMMA INT R_PARENTHESIS )* R_BRACE
lambda --> 'fun' L_PARENTHESIS var R_PARENTHESIS L_BRACE expr R_BRACE
map --> 'map' L_PARENTHESIS lambda COMMA expr R_PARENTHESIS
filter --> 'filter' L_PARENTHESIS lambda COMMA expr R_PARENTHESIS
intersert --> 'intersect' L_PARENTHESIS expr COMMA expr R_PARENTHESIS
concat --> 'concat' L_PARENTHESIS expr COMMA expr R_PARENTHESIS
union --> 'union' L_PARENTHESIS expr COMMA expr R_PARENTHESIS
star --> L_PARENTHESIS expr R_PARENTHESIS '*'
COMMA --> ','
QUOTE --> '"'
L_BRACE --> '{'
R_BRACE --> '}'
L_PARENTHESIS --> '('
R_PARENTHESIS --> ')'
EOL --> ';'
ID_CHAR --> '_' | [a-z] | [A-Z]
INT --> [1-9][0-9]* | '0'
BOOL --> 'true' | 'false'
```
### Пример скриптов
1. Загрузка графа
2. Получение финальных вершин в переменную `vertices`
3. Назначение стартовыми всех вершин
4. Печать `vertices`
5. Печать меток обновленного графа
```
graph = load_graph("p/a/t/h");
vertices = get_final(graph);
graph_upd = set_start(get_vertices(graph), graph);
print vertices;
print get_labels(graph_upd);
```
1. Загрузка графа
2. Получение всех ребер графа
3. Назначение финальными вершинами стартовые
4. Печать финальных вершин
5. Печать ребер
```
graph = load_graph("p/a/t/h/2");
edges = get_edges(graph);
graph_upd = set_final(get_start(graph), graph);
print get_final(graph_upd);
print edges;
```
1. Регулярный запрос
2. Регулярный запрос, использующий предыдущий
3. печать конкатенации используемых регулярных запросов
```
a = union ("A", "a");
b_a = (union ("b", a))*;
print concat (a, b_a);
```
