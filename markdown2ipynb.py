import sys
from fn import Stream, _
from fn.iters import splitby, head, accumulate
from itertools import * 
from typing import *
import json
#NOTE: couldn't use `splitby` with `Stream` . . . 
MarkdownBlock = NamedTuple('MarkdownBlock', [('content', str)])
PythonBlock = NamedTuple('PythonBlock', [('content', str)])
Cell = Union[MarkdownBlock, PythonBlock]
def read_markdown(lines: Iterable[str]) -> Cell:
    if not lines:
        return [] 
    if lines[0].startswith("```python"):
        codeLines, rest = splitby(lambda x: not x.startswith("```"), lines[1:])
        codeLines = list(codeLines)
        rest = list(rest)[1:]
        res =  PythonBlock(codeLines)
    else:
        mdLines, rest = splitby(lambda x : not x.startswith("```python"), lines)
        mdLines, rest = list(mdLines), list(rest)
        res = MarkdownBlock(mdLines)
    return [res] + read_markdown(rest)


bigTemplate = {   "cells" : [],  "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
def process(fn: str): # -> Unit:
    #lines = Stream() << open(fn)
    lines = list(open(fn))
    rawBlocks = read_markdown(lines)
    isPyBlocks = list(map(lambda x: isinstance(x, PythonBlock), rawBlocks))
    # weird hack to get around accumulate not allowing start args
    inputNums = list(accumulate([False] + isPyBlocks, lambda acc, x: acc  + int(x)))[1:]
    cells = list(map(get_temlate, rawBlocks, inputNums))
    bigTemplate['cells'] = cells
    print(json.dumps(bigTemplate))
    
def get_temlate(cell, count):
    if isinstance(cell, PythonBlock): return     {
           "cell_type": "code",
           "execution_count": count,
           "metadata": {
               "collapsed": True
               },
           "outputs": [],
        "source" : cell.content}
    if isinstance(cell, MarkdownBlock): return {
           "cell_type": "markdown",
           "metadata": {},
           "source" : cell.content
        }        
if __name__ == '__main__': process(sys.argv[1])
