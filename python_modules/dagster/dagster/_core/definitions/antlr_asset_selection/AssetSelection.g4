grammar AssetSelection;

start: expr EOF;

// Root rule for parsing expressions
expr
    : assetExpr                                    # AssetExpression
    | attributeExpr                                # AttributeExpression
    | traversal expr                               # UpTraversalExpression
    | traversal expr traversal                     # UpAndDownTraversalExpression
    | expr traversal                               # DownTraversalExpression
    | NOT expr                                     # NotExpression
    | expr AND expr                                # AndExpression
    | expr OR expr                                 # OrExpression
    | functionName LPAREN expr RPAREN              # FunctionCallExpression
    | LPAREN expr RPAREN                           # ParenthesizedExpression
    ;

// Traversal operators
traversal
    : STAR
    | PLUS+
    ;

// Function names as tokens
functionName
    : SINKS
    | ROOTS
    ;

// Attribute expressions for specific attributes
attributeExpr
    : TAG COLON value (EQUAL value)?               # TagAttributeExpr
    | OWNER COLON value                            # OwnerAttributeExpr
    | GROUP COLON value                            # GroupAttributeExpr
    | KIND COLON value                             # KindAttributeExpr
    | CODELOCATION COLON value                     # CodeLocationAttributeExpr
    ;

// Define the EQUAL token for tag:value=value syntax
EQUAL : '=';

// Value can be a quoted or unquoted string
value
    : QUOTED_STRING
    | UNQUOTED_STRING
    ;

// Asset expressions
assetExpr
    : QUOTED_STRING                                # ExactMatchAsset
    | UNQUOTED_STRING                              # PrefixMatchAsset
    ;

// Tokens for operators and keywords
AND : 'and';
OR : 'or';
NOT : 'not';

STAR : '*';
PLUS : '+';

COLON : ':';

LPAREN : '(';
RPAREN : ')';
COMMA : ',';

// Tokens for keys
OWNER : 'owner';
GROUP : 'group';
TAG : 'tag';
KIND : 'kind';
CODELOCATION : 'codelocation';

// Tokens for function names
SINKS : 'sinks';
ROOTS : 'roots';

// Tokens for strings
QUOTED_STRING : '"' (~["\\\r\n])* '"' ;
UNQUOTED_STRING : [a-zA-Z_][a-zA-Z0-9_]*;

// Whitespace
WS : [ \t\r\n]+ -> skip ;