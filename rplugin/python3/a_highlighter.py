import neovim
import re


def find_function_definition(source, func_name):
    lines = source.split('\n')

    in_function = False
    for index, line in enumerate(lines):
        if re.match(r'def {0}'.format(func_name), line):
            in_function = True
            start = index

        # This won't work with multiple returns
        if in_function:
            if re.match(r'.*return.*', line):
                end = index
                break

    definition = {
        'start': start,
        'end': end,
        'source': lines[start:end]
    }
    return definition


def determine_function_arguments(source: str, func_name: str):
    line = find_function_definition(source, func_name)['source'][0]

    start_index = line.index('(') + 1
    end_index = len(line) - 2

    return line[start_index:end_index].split(', ')


def find_argument_uses(source: str, func_name: str):
    definition = find_function_definition(source, func_name)
    arguments = determine_function_arguments(source, func_name)

    lines = definition['source']
    print(lines)

    findings = {}
    for index, line in enumerate(lines):
        # TODO: Bad regex
        if re.match(r'[\s]*#\s*', str(line)):
            continue

        for arg in arguments:
            res = re.search(r'\b{0}\b'.format(arg), line)
            if res:
                # print('WOW I FOUND A MATCH:', arg, '|', line)
                # print(res.start(), res.end())

                if arg not in findings.keys():
                    findings[arg] = []

                findings[arg].append([definition['start'] + index + 1, res.start() + 1, res.end() - res.start()])

    return findings


@neovim.plugin
class HighlighterPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command("AHighlighter", range='', nargs='*')
    def highlight_the_things(self, args, range):
        buffer = self.nvim.current.buffer
        source = ('\n').join(buffer)
        results = find_argument_uses(source, args[0])

        self.nvim.current.line = str(results)

        for keyword in results.keys():
            self.nvim.command('call matchaddpos("GruvboxAqua", {0})'.format(str(results[keyword])))

    # This is from chromatica.nvim
    # This gives a pretty good idea about how to highlight I think.
    # And I'm quite sure it's async
    def _highlight(self, filename, lbegin=1, lend=-1):
        """internal highlight function"""
        _lbegin = lbegin
        _lend = self.vimh.line("$") if lend == -1 else lend

        buffer = self.__vim.current.buffer
        tu = self.ctx[filename]["tu"]

        self.profiler.start("_highlight")
        syn_group = syntax.get_highlight(tu, buffer.name, _lbegin, _lend)

        for hl_group in syn_group:
            for pos in syn_group[hl_group]:
                _row = pos[0] - 1
                col_start = pos[1] - 1
                col_end = col_start + pos[2]
                buffer.add_highlight(hl_group, _row, col_start, col_end,\
                        self.syntax_src_id, async=True)
        self.profiler.stop()
