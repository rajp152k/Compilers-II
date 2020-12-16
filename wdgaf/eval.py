from pathlib import Path
from lark import Lark
from random import choice
import argparse
prs = argparse.ArgumentParser()
prs.add_argument('--src',help='.fu source file',default=None)
args = prs.parse_args()


# importing grammar
fg = Path('./grammar/grammar.lark')
assert(fg.is_file())
with open(fg,'r') as f:
    grammar_raw = f.read()


if args.src is None:
    source = choice(list((Path()/'tests').glob('**/*.fu')))
    # tests on a random source from test
else:
    source = Path('.')/f'{args.src}'

assert(source.is_file() and source.suffix == '.fu')
print(f'testing {source.name}')

with open(source,'r') as f:
    code_raw = f.read()

# quick eval code for now: pretty prints program tree 

parser = Lark(grammar_raw)
print(parser.parse(code_raw).pretty())
