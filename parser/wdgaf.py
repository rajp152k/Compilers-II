# necessary imports
import sys
import logging
from pathlib import Path
from lark import Lark
import lark
from modules.process_tree import ProcessTree
from modules.fu_config import config
import argparse

# driver function
def main():
	# set level to critical
	logging.getLogger().setLevel(logging.CRITICAL)

	# Import grammar and create parser
	grammar = Path('./grammar/grammar.lark')
	assert(grammar.is_file())
	with open(grammar,'r') as f: raw_grammar = f.read()
	# create the parser instance 
	parser = Lark(raw_grammar, parser="lalr", transformer=ProcessTree())

	# create argument parser
	args_parser = argparse.ArgumentParser(description='Interpreter for WDGAF language', epilog="And that's how you use the interepreter")
	args_parser.add_argument('src', metavar='src', help='source file path')
	args_parser.add_argument('-v', '--verbose', help="generates verbose output", action="store_true")

	# get the arguments
	args = args_parser.parse_args()

	# configure verbose parametere here!
	# this is used in all other modules!
	config['verbose'] = args.verbose

	# check if source file is provided
	if args.src: source = Path(args.src)
	else: print("Usage:\npython wdgaf.py <filename>"); sys.exit();

	# assert that file exist and it's *.fu file
	assert(source.is_file() and source.suffix == '.fu')
	# read the source file
	with open(source,'r') as f: code_raw = f.read()

	# execute user code
	try:
		parser.parse(code_raw)

	# TODO: parsing error needs to be customized
	except lark.exceptions.UnexpectedToken as unexpToken:
		print(unexpToken)

	# these exceptions will generally be well-defined
	except Exception as ex:
		print(ex)


# invoke the driver function
main()