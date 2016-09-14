from function_arguments import determine_function_arguments, find_argument_uses


my_source_file = '''
# wow a comment

a = 13

# another comment thing

def my_function(a, b, bbb):
    if a:
        d = b + 3 + b
    else:
        d = b

        # comment with b in it

    return a + b + bbb + d

# This comment

b = 12

'''

multiple_funcs = '''
def other_function(a, b, c):
    if a:
        d = b + 5 + b
    else:
        d = c

        # comment with b in it

    return a + d

def my_function(a, b, c):
    if a:
        d = b + 3 + b
    else:
        d = b

        # comment with b in it

    return a + b + c + d
'''


class TestFunctionArguments:
    def test_determine_function_arguments(self):
        result = determine_function_arguments(my_source_file, 'my_function')
        assert result == ['a', 'b', 'bbb']

        uses = find_argument_uses(my_source_file, 'my_function')
        import pprint
        pprint.pprint(uses)

    def test_multiple_functions(self):
        result = determine_function_arguments(multiple_funcs, 'my_function')
        assert result == ['a', 'b', 'c']
