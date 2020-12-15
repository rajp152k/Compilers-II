import sys
import os
import logging
import warnings
from pathlib import Path
from lark import Lark
import lark
from modules.process_tree import ProcessTree
from modules.fu_config import config
import argparse

import wdgaf

def main():
    # setup mechanism for any meta-requirements in the close future
    wdgaf.driver()

if __name__ == '__main__':
    main()
