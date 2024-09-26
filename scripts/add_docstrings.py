import ast
import astor

class DocstringAdder(ast.NodeTransformer):
    """AST NodeTransformer that adds structured docstrings to functions and classes."""

    def visit_FunctionDef(self, node):
        """Add structured docstring to functions."""
        if not ast.get_docstring(node):
            # Generate argument details
            args = [arg.arg for arg in node.args.args]
            arg_str = ""
            for arg in args:
                arg_str += f"        {arg} (type): Description of {arg}.\n"

            # Generate the docstring with Args and Returns placeholders
            docstring = (
                '"""\n'
                "        Description of the function.\n\n"
                "        Args:\n"
                f"{arg_str}\n"
                "        Returns:\n"
                "            type: Description of return value.\n"
                '        """'
            )

            # Insert the docstring as the first element in the function's body
            docstring_node = ast.Expr(value=ast.Constant(value=docstring))
            node.body.insert(0, docstring_node)

        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        """Add structured docstring to classes."""
        if not ast.get_docstring(node):
            # Generate a placeholder docstring for the class
            docstring = (
                '"""\n'
                "        Helper class for operations.\n"
                '        """'
            )
            
            # Insert the docstring as the first element in the class body
            docstring_node = ast.Expr(value=ast.Constant(value=docstring))
            node.body.insert(0, docstring_node)
        
        self.generic_visit(node)
        return node

def add_docstrings_to_file(file_path):
    """Read a Python file, add structured docstrings, and save to a new file suffixed with '_doc'."""
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create an instance of the transformer and apply it to the AST
    transformer = DocstringAdder()
    transformed_tree = transformer.visit(tree)

    # Convert the AST back to source code
    new_source_code = astor.to_source(transformed_tree)

    # Create a new file name suffixed with '_doc'
    new_file_path = file_path.replace('.py', '_doc.py')

    # Write the modified source code to the new file
    with open(new_file_path, 'w') as new_file:
        new_file.write(new_source_code)

    print(f"Processed file: {new_file_path}")


# Example usage
add_docstrings_to_file('/Users/frankserrao/MyStuff/TestAndPlay/Click2Mail/c2m-generative-ai-marketing-portal/assets/layers/utilities/python/aws_helper.py')
