grammar GQL;

prog:	(stmt EOL NEWLINE?)* EOF ;

stmt:   var '=' expr
    |   'print' expr
    ;

var:    ID_CHAR string ;
string: (ID_CHAR | '/' | '.' | INT)* ;


expr:	L_PARENTHESIS expr R_PARENTHESIS
    |   var
    |   val
    |   map
    |   filter
    |   intersect
    |   concat
    |   union
    |   star
    ;

val:    L_PARENTHESIS val R_PARENTHESIS
    |   QUOTE string QUOTE
    |   INT
    |   BOOL
    |   graph
    |   vertices
    |   labels
    |   edges
    ;

graph:  'set_start' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
    |   'set_final' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
    |   'add_start' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
    |   'add_final' L_PARENTHESIS vertices COMMA graph R_PARENTHESIS
    |   'load_graph' L_PARENTHESIS path R_PARENTHESIS
    |   var
    ;

path:   QUOTE string QUOTE
    |   var
    ;

vertices:   'get_start' L_PARENTHESIS graph R_PARENTHESIS
        |   'get_final' L_PARENTHESIS graph R_PARENTHESIS
        |   'get_reachable' L_PARENTHESIS graph R_PARENTHESIS
        |   'get_vertices' L_PARENTHESIS graph R_PARENTHESIS
        |   L_BRACE INT (COMMA INT)* R_BRACE
        |   var
        |   EMPTY_SET
        ;

labels: 'get_labels' L_PARENTHESIS graph R_PARENTHESIS
    |   L_BRACE (QUOTE string QUOTE | INT | var) (COMMA (QUOTE string QUOTE | INT | var))* R_BRACE
    |   EMPTY_SET
    ;

edges:  'get_edges' L_PARENTHESIS graph R_PARENTHESIS
    |   L_BRACE L_PARENTHESIS INT COMMA (val | var) COMMA INT R_PARENTHESIS ( COMMA L_PARENTHESIS INT COMMA (val | var) COMMA INT R_PARENTHESIS )* R_BRACE
    |   EMPTY_SET
    ;


lambda: 'fun' L_PARENTHESIS var R_PARENTHESIS L_BRACE expr R_BRACE ;
map:    'map' L_PARENTHESIS lambda COMMA expr R_PARENTHESIS ;
filter: 'filter' L_PARENTHESIS lambda COMMA expr R_PARENTHESIS ;

intersect   :  'intersect' L_PARENTHESIS expr COMMA expr R_PARENTHESIS ;
concat      :   'concat' L_PARENTHESIS expr COMMA expr R_PARENTHESIS ;
union       :   'union' L_PARENTHESIS expr COMMA expr R_PARENTHESIS ;
star        :   L_PARENTHESIS expr R_PARENTHESIS '*' ;

COMMA: ',' ;
QUOTE: '"' ;
L_BRACE: '{';
R_BRACE: '}';
L_PARENTHESIS: '(' ;
R_PARENTHESIS: ')' ;
EOL: ';' ;
EMPTY_SET: 'set()';
WS: ([ \t\n\r\f] | ('/*' ~[\r\n]* '*/')) -> skip;
NEWLINE : [\r\n]+ -> skip ;
ID_CHAR : '_' | [a-z] | [A-Z] ;
INT     : '-'? [1-9][0-9]* | '0' ;
BOOL    : 'true' | 'false'  ;
