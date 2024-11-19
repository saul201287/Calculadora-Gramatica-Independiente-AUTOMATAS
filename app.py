from flask import Flask, render_template, request, jsonify
import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph
import uuid

app = Flask(__name__)

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'
t_NUMBER = r'\d+(\.\d+)?'  

def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = ('BINOP', p[2], p[1], p[3])
def p_number(p):
    'number : NUMBER'
    p[0] = float(p[1])
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('BINOP', p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('NUM', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Error de sintaxis")

parser = yacc.yacc()

@app.route('/')
def index():
    return render_template('index.html')

def create_grammar_tree_visual(tree):
    """
    Genera un grafo que muestra la derivación de la gramática
    desde el árbol generado por PLY.
    """
    graph = Digraph(format='png')
    graph.attr(dpi='300')

    def add_nodes_edges(tree, parent_id=None):
        if not tree:
            return

        node_id = str(uuid.uuid4())

        if tree[0] == 'NUM':
           label = str(tree[1])  
        elif tree[0] == 'BINOP':
           label = tree[1]  
        else:
           label = tree[0]

        graph.node(node_id, label)

        if parent_id:
           graph.edge(parent_id, node_id)

        if len(tree) > 2:  
           add_nodes_edges(tree[2], node_id)
           add_nodes_edges(tree[3], node_id)


    add_nodes_edges(tree)
    return graph

@app.route('/generate_tree', methods=['POST'])
def generate_tree():
    try:
        expression = request.json.get('expression', '')
        if not expression:
            return jsonify({'error': 'Expression is empty'}), 400

        tree = parser.parse(expression)
        if not tree:
            return jsonify({'error': 'Invalid expression'}), 400

        graph = create_grammar_tree_visual(tree)
        filename = graph.render(filename='static/tree', cleanup=True)

        return jsonify({'tree_image': 'tree.png'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
