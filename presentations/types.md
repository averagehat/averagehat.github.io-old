__Mypy:  A New Hope?__



---

* I make commandline apps for biologists.
* In python.

---

[A recent pep](https://www.python.org/dev/peps/pep-0484/) solidifies type annotations in python 2 and 3. These type annotations are compatible with python 2 & 3
* ignored altogether
* used however you wish in your own program, or 
* used to typecheck your code with [mypy](github.com/python/mypyp).

---

###Vanilla Python

```python
>>> "foo" > sys.maxint
 True # sure, why not?
```
```python
>>> 3.0 == 3
True
```

```python
doesntHaveAttribute = object

x = doesntHaveAttribute.attribute 

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-3-662d1f2b981a> in <module>()
----> 1 foo.attribute
```
python will . . . 
---

Blow up all the time.

---

Dynamic typing is hard.

---

What's in a type?

---

bool = $\{ True, False \}$

int ==  $ \mathbb{Z} $

char == $\{ 'a'...'z' \}$

str == $\{ x* | x \in char \}$

nonetype = $\{ None \}$

---

Poor $f(x)$ just wants to do its job.

But $x$ . . . 

---

$ x \in \mathbb{Z} \bigcup \{'a','b'...\} \bigcup \{True,False} \bigcup \{ x* | x \in char \} \bigcup \{ None \} $ ...

---

If we assume that $x$ is in a specific set, the domain is still large. 

```python
In [1]: -sys.maxint -1
Out[1]: -9223372036854775808

{'a', 'aa', 'ab', 'ba', ..... }
```

--- 

The co-domain of $f$ (its return value) is also unbounded. API's can behave unexpectedly.

Exceptions are a part of this.

```python
ValueError  Traceback (most recent call last)
```

. . . $\bigcup$ GOTO

---

A program (data) can have a huge number of possible states.
* Unit testing cherry-picks form our program's possible states and makes sure they work.
* Static typing limits the possible states of our program.

---

###mypy
* started as a statically-typed language with python sytax
* requires python 3 (but can typecheck python 2)
* similar in vein to typescript/flow

---

```python
from typing import * 

List[float]     # [1.0, 2.3]

Tuple[int, str] # (1, "foo")

Dict[str, bool] # {'a' : False}

Callable[[List[int]],int] # lambda xs: sum(xs)/len(xs)

NamedTuple("Point", [('x', int), ('y', int)]) # Point(x=1, y=3)
```

---

###Functions
```python
def add(x: int, y: int) -> int:
   return x + y

A = TypeVar("A")
B = TypeVar("B")
def map(f: Callable[[A],B], xs: List[A]) -> List[B]:
  . . . .
```

---

python 2
```python
def map(f, xs): # type: (Callable[[A],B], List[A]) -> List[B]
   # could be down here
```

---

###Generics

```python
class Option(Generic[T]):
    def getOrElse(t: T) -> T:
       . . . 
```

---

"Free" type errors 

```python
x = 12 

x + "Eureka"
error: Unsupported operand types for + ("float" and "str")
```

---

Local inference

```python
point = Point(1, 3)
x = point.x # mypy infers the type after assignment

x > "Eureka"
error: Unsupported operand types for > ("float" and "str")
```

---

#Standard library

```python 
map("not-a-function", [1, 2, 3])

error: Argument 1 to "map" has incompatible type "str"; 
expected Callable[[int], None]
```

---

###Ducked Typing
```python
len(3)

error: Argument 1 to "len" has incompatible type "int";
expected "Sized"
```

---

More type errors when you work for it.

---

`NamedTuple` 
* Immutable
* Easy

---

Product type!
(think cartesian product)

```python
Point3D = NamedTuple("Point3D", 
                    [("x", int), 
                     ("y", int), 
                     ("z", int)])

```
Point3D = $ \mathbb{Z} \times \mathbb{Z} \times \mathbb{Z} $
. . . with names.

---

```python 
RobotLegs = NamedTuple("RobotLegs", 
                      [("leftLeg", List[Point3D]), 
                       ("rightLeg", List[Point3D]), 
                       ("color", str)])
```
RobotLegs = List $\times$ List $\times$ str

It is a list AND another list AND a string.

. . . plus its name, (constructor) which makes it its own type.


--- 


Invalid states!
```python 
RobotLegs = NamedTuple("RobotLegs", 
                      [("leftLeg", List[Point3D]), 
                       ("rightLeg", List[Point3D]), 
                       ("color", str)])
``` 
* negative 3D coordinates
* gibberish `color`
* other stuff

---

```python
blueRobot = RobotLegs(points, points, "fizbizzle")
```

```python
def getColor(legs: RobotLegs) -> int:
    if legs.color not in ["skyblue", "red", "white"]:
        raise ValueError("Invalid color %s" % legs.color)
    else:
         . . . . 
```
(What if we forget to check?)

The set of `str` is too big for `color` . . . 

---

###Union

```python
SkyBlue = NamedTuple("SkyBlue", [])
PastelRed = NamedTuple("PastelRed", [])
White = NamedTuple("White", [])

Color = Union[SkyBlue, PastelRed, White] 
```
Color = blue OR red OR white

Color = $ blue \bigcup red \bigcup white $

---

```python
def getColor(color: Color) -> int:

    if isinstance(color, SkyBlue): 
        return 0x87CEFA

    elif isinstance(color, PastelRed): 
        return 0x9F89

    else:  return 0x000
```

---

Product Type

$A \times B$

$0 * 1$   (AND)

---

Sum Type 

* $A \bigcup B$

* $0 + 1$   (OR)


---

More complex types (ADTs)

```python
Rifle = NamedTuple('Rifle', 
                   [('ammo' , int), 
                    ('model' , str)])

Knife = NamedTuple('Knife', 
                 [('shape' , List[Point3D]), 
                  ('isSharp', bool)])

weapon = Union[Rifle, Knife]

# note that RobotArms is also its own type.  
GiantRobot = NamedTuple('GiantRobot', 
                      [('weapon', Weapon), 
                       ('legs' , RobotLegs),
                       ('arms', RobotArms)])
```

---

###Dispatch union types
```python
def canFight(robot: GiantRobot) -> bool:
    if isinstance(robot.weapon, Rifle): # type inference happens here
        return robot.weapon.ammo > 0
    else: 
        return robot.weapon.isSharp
....
#without `isinstance`: 
note: In function "canFight":
  error: Some element of union has no attribute "ammo"
```

---

We want non-negative coordinates . . . 

type posInt = $\mathbb{N}$

not possible. Instead . . . 

---

```python
class Point3D(object):
    def __init__(self, x: float, y: float, z: float) -> None:
        assert x >= 0 and y >= 0 and z >= 0
        self.x = x
        self.y = y
        self.z = z
```

But . . . 

---

```python
p = Point3D(0, 1.0, 2.9) # okay
p.x = -sys.maxint  # :(
```
Mutability!

So . . . 

---

```python
class SafePoint3D(Point3D):
    def __new__(self, x: float, y: float, z: float) -> SafePoint3D:
        assert x >= 0 and y >= 0 and z >= 0
        self = super(self, Point3D).__new__(self, (x, y, z))
        return self
```

---

* We know where a `SafePoint3D` comes from
* We limited the size of the set
* Functions which accept `SafePoint3D` are guaranteed that it will represent a valid state 

---

But... 

---

```python
class NotSoSafePoint3D(SafePoint3D):
    def __new__(self, x: float, y: float, z: float) -> SafePoint3D:
        assert x != 0
        self = super(self, Point).__new__(self, (x, y, z))
        return self
``` 
Inheritance!

So . . . 

---

```python
from typing import Final
class SafePoint3D(Point3D, metaclass=Final)
   # etc.
```
* throws a runtime error if you try to subclass `SafePoint3D`.

* *Still* possible to circumvent this

---

###Achieved (?)
* Modelled our data
* (some) Safety
* Documentation
* Separated validation code: 
    * function domains are smaller
    * code is easier to test

---

Limitations
* Less powerful than pattern matching
    * attribute with same name and type
    * non-exhaustive (so far)
    * uglier
* Implicit null (for now)
* Subclassing kills safety (if your types allow it)
* Python is mostly mutable
* Not "idiomatic"

---

###Fun things

* Commandline dispatch
* testing
* declarative pipelines

---

docopt

```python
"""
Usage:
     grep_tweets <url> <words>... [ --ignore-case ] [ -n <count> ] --output <output> 
Options:
    --output=<output>         output file
    -n=<count>                number of tweets
"""
```

---

docopt
```
def run(url, count, output, ignore_case):
    . . . 

scheme = Schema({ 'url' : is_url,
      '-n' : Use(int),
      '--ignore-case' : lambda _: True,
      '--output' : lambda _: True,
      'words' : lambda _: True }
# entry point
raw_args = docopt(__doc__, version='Version 1.0')
args = scheme.validate(raw_args) 
. . . 
run(args['--url'], args['words'], args['-n'], args['--output'], args['--ignore-case'])
```

---

Argparse

```python
parser = argparse.ArgumentParser()
parser.add_argument('url') 
parser.add_argument('words', nargs='+') 
parser.add_argument('-n', type=int)
parser.add_argument('--output', required=True)
parser.add_argument('--ignore-case', 
                    action='store_true', default=False)
# entry point
args = parser.parse_args() 

. . . 
run(args.url, args.words, args.n, arg.output, args.ingore_case)
```

---

mypy-extras
```python
from path import Path 
class Url . . .  

GrepTweetOptions = \
     NamedTuple("GrepTweetOptions",
              [('n', Optional[int]),
               ('output', Path),
               ('ignore_case', bool)])

def run(url: Url, words: List[str], options: GrepTweetOptions) -> None:
    . . . 
```

---

mypy-extras
```python
# entry point
args = dispatch_from_type(run)
run(**args)
```

---

* Most of the code is types.
* (types are good).
* Validation happens in one place.
* Validation is guaranteed.
* Our `run` function is always synced with our user interface.

---

How can we achieve this?

A type is a Tree with different kinds of branches.

* `Union` is one kind of branch.
* `NamedTuple` is another kind.
* etc. . . . 

use `argparse` to fill in the parsing and usage (or not)

---

```python 
def type_to_argparse(t: type, p: ArgumentParser) -> Dict[str,Any]:
   primitives  = [int, str, float, unicode, bytes]

   if t == bool:
        return dict(action='store_true')

   elif t in primitives: 
       return dict(type=t)

   elif is_enum(t):
       raise ValueError("Enum types not allowed outside of Union.")

   elif is_namedtuple(t):
       for name, typ in t._field_types.items():
           d = type_to_argparse(typ, p)
           if 'required' not in d and d.get('action') != 'store_true':
               d['required'] = True
           p.add_argument('--'+name, **d) 

. . . etc.
```

---

todo: mutually exclusive arguments?

---

###Testing

```python
In [0]: !pip install hypothesis
In [1]: from hypothesis import strategies as st
In [2]: st.integers().example()

    1070630604996546757468194856009676754204344532158L
```
strings, dictionaries, lists, etc.

---

```python
@given(atype, atype)
def test_union_is_either(self, t1, t2):
    union = Union[t1, t2]
    self.assertIsInstance(t1, union)
    self.assertIsInstance(t2, union)
```

--- 

mypy-extras
```python
@given(type_to_strat(Robot)):
test_robot_with_ammo_can_fight(self, robot):
    assume(isinstance(robot.weapon, Rifle))
    assume(robot.weapon.ammo != 0)
    self.assertTrue(canFight(robot))

@given(type_to_strat(Robot)):
test_legs_not_overlap_arms(self, robot):
    self.assertNotEqual(robot.legs, robot.arms)
```
* If we change legs, the ammo test won't break.
* "Exhaustive" testing (sort of)
*  $\| bool \times Color \| = 8$

---

mypy-extras (Functions)

```python
def mod_list(m: int, xs: List[int]) -> List[int]:
    return list(map(lambda x: x % m, xs))

my_func_strategy = func_strategy(example_func)

@given(my_func_strategy)
def test_example_func(self, args):
    assume(args['m'] > 0)
    result = mod_list(**args)
    less_than_m = map(lambda x: x < args['m'], result)
    self.assertTrue(all(less_than_m))
``` 

---

```make

sorted.json: sorted.csv
   . . . . 
sorted.csv: grepped.txt
   . . . . 

grepped.txt: foo.txt
   grep "(she|her|girl|female|woman)" $< > $@

foo.txt: 
   wget $(URL)
```   
   
---


```python
class TextFile(Path): pass 
. . .

def download(url: Url) -> TextFile

def to_csv(lines: List[str]) -> CSV

def grep(txt: TextFile) -> List[str]

def csv_to_json(csv: CSV) -> JSON

```

---

```python
#entry point
to_json( to_csv( grep( download( url) ) ) ) 
```

Typechecks!

Or . . . 

---

A -> B 

B -> C

C -> D

given $x \in A$ and wanting $D$:

A -> B -> C -> D

---

```python
class TextFile(Path): pass 
. . .

def download(url: Url) -> TextFile

def to_csv(lines: List[str]) -> CSV

def grep(txt: TextFile) -> List[str]

def csv_to_json(csv: CSV) -> JSON 
```
given a url as input . . . 

url -> TextFile -> List[str] -> CSV -> JSON

---

```python
def get_pos_opt_args(func: Callable[...,Any]) -> Node:
    annotations = func.__annotations__
    is_opt = lambda x: x[0] == 'opts' # type: Callable[[Tuple[str,type]], bool]
    pos_args, opt_args = partition(is_opt, annotations.items()) 
    return func, dict(pos_args), dict(opt_args)

def order_funcs(funcs: List[Callable[...,Any]], input: Union[File, Tuple[File,File]]) -> List[Node]:
    nodes = map(get_pos_opt_args, funcs)
    def fill_opts(node: Node) -> Callable[...,Any]:
        f, _, optargs = node
        if not optargs: return node
        assert len(optargs) == 1
        return partial(f, **{next(iter(optargs.keys())) :  None}) , _, optargs
    filled_nodes = list(map(fill_opts, nodes)) 
. . . .
```

---

```python
    def top_sort(acc: List[Node], to_go: List[Node]) -> List[Node]:
        if to_go == []: returnacc
        def is_satisfied(node: Node) -> bool:
            f, args, _ = node
            required = keyfilter(lambda x: x != 'return', args) 
            get_ret = lambda x: x[1]['return'] # type: Callable[[Node],type]
            acc_rets = map(get_ret, acc)
            acc_rets = list(acc_rets)
            satisfied = all([(t in acc_rets) for t in required.values()])
            return satisfied
        satisfied = list(filter(is_satisfied, to_go))
        nextnode, next_to_go = satisfied[0], satisfied[1:]
        return top_sort([nextnode] + acc, next_to_go)
    sorted = top_sort([input], filled_nodes)
    return sorted
```
```python
def build_pipeline(funcs: List[Callable[...,Any]], input) -> Callable[...,Any]:
    nodes = order_funcs(funcs, input)
    ordered_funcs = map(get(0), nodes)
    return reduce(compose, ordered_funcs)
```

---

```python
#entry point
funcs = [csv_to_json...]
build_pipeline(funcs, input)()
```

---

Branching with Error (or whatever) unions
```python
FailedDownload = NamedTuple("FailedDownload",
                          [('time', int),
                           ('url', Url)])

PossibleDownload = Union[TextFile, FailedDownload]

def download(url: Url) -> PossibleDownload
 
def one_road(txt: TextFile) -> MoreFiles

def another_road(fd: FailedDownload) -> SomethingElseEntirely 
```

---

* Declarative, like `Make` (but more powerful?)

* *Not* typesafe

---

###Questions?

[@__averagehat](https://twitter.com/__averagehat)

[github.com/averagehat/mypy-extras/](https://github.com/averagehat/mypy-extras/)

