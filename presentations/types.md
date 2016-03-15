
### Some things with mypy: sum and product types
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

---

Blow up all the time.

---

Dynamic typing is hard.

You're domain is big . . . 

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

$ x \in \mathbb{Z} \bigcup \{'a','b'...\} \bigcup \{True,False} \bigcup \{ x* | x \in char \} \bigcup \{ None \} \bigcup object $

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


###mypy
* started as a statically-typed language with python sytax
* requires python 3 (but can typecheck python 2)
* similar in vein to typescript/flow

---

```python
from typing import * 
List[float] # [1.0, 2.3]
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
def map(f: Callable[[A],B], List[A]) -> List[B]:
  . . . .
```

---

###Generics

```python
class Option(Generic[T]):
    def getOrElse(t: T) -> T:
       . . . 
```

---

Free type-errors (at "compile time")

```python
NamedTuple("Point", [('x', int), ('y', int)]) # Point(x=1, y=3)
point = Point(1, 2)

point.x + "Eureka"
foo.py:10: error: Unsupported operand types for + ("float" and "str")

x = point.x # mypy infers the type after assignment

x > "Eureka"
foo.py:10: error: Unsupported operand types for > ("float" and "str")
```

---

```python 
map("not-a-function", [1, 2, 3])

foo.py:7: error: Argument 1 to "map" has incompatible type "str"; expected Callable[[int], None]
```

---

```python
len(3)

foo.py:8: error: Argument 1 to "len" has incompatible type "int"; expected "Sized"
```

---

More type errors when you work for it.

`NamedTuples` (Product Type)
* Immutable
* Easy

---

```python
Point3D = NamedTuple("Point3D", 
                    [("x", float), 
                     ("y", float), 
                     ("z", float)])

RobotLegs = NamedTuple("RobotLegs", 
                      [("leftLeg", List[Point3D]), 
                       ("rightLeg", List[Point3D]), 
                       ("color", str)])
```

---

Invalid states!
* gibberish `color`
* negative 3D coordinates
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
* What if we forget to check?

The set of `str` is too big for `color` . . . 

---

###Union

```python
SkyBlue = NamedTuple("SkyBlue", [])
PastelRed = NamedTuple("PastelRed", [])
White = NamedTuple("White", [])

Color = Union[Blue, PastelRed, White]

RobotLegs = NamedTuple("RobotLegs", 
                     [("leftLeg", List[Point3D]),
                      ("rightLeg", List[Point3D]), 
                      ("color", Color)])
```

```python
def getColor(legs: RobotLegs) -> int:
    colorsToInts = { SkyBlue() : 0x87CEFA }
    return colorsToInts.get(legs.color)
```

---

NamedTuple = Product Type

$A \times B$

$0 * 1$ (and)

Union  =  Sum Type 

* $A \bigcup B$

* $0 + 1$ (or)

---

Back to our robots. We want non-negative coordinates . . . 

posint = $\mathbb{N}$

not possible. Instead . . . 

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
class SafePoint3D(object):
    def __new__(self, x: float, y: float, z: float) -> SafePoint3D:
        assert x >= 0 and y >= 0 and z >= 0
        return Point3D(x, y, z)
```

But... 

---

```python
class NotSoSafePoint3D(SafePoint3D):
    def __new__(self, x: float, y: float, z: float) -> SafePoint3D:
        assert x != 0
        return Point3D(x, y, z)
``` 
Inheritance!

So . . . 

---

```python
from typing import Final
class SafePoint3D(Final, object):
   # etc.
```
* We know where a `SafePoint3D` comes from
* We limited the size of the set
* Functions which accept `SafePoint3D` are guaranteed that it will represent a valid state 

---

###More complex types (ADTs)

```python
Rifle = NamedTuple('Rifle', 
                   [('ammo' , int), 
                    ('model' , str)])

Knife = NamedTuple('Knife', 
                 [('shape' , List[SafePoint3D]), 
                  ('isSharp', bool)])

weapon = Union[Rifle, Knife]

# note that RobotArms is also its own type.  
RobotArms = NamedTuple("RobotArms", 
                     [("leftArm", List[SafePoint3D]), 
                     ("rightArm", List[SafePoint3D]), 
                     ("color", Color)])

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
```
without `isinstance`....  

```python
foo.py: note: In function "canFight":
foo.py:35: error: Some element of union has no attribute "ammo"
```

---

###Achieved
* Safety
* Documentation
* Separated validation code: 
    * function domains are smaller
    * code is easier to test

---

We really want to make it is easy on ourselves and be *really really sure* that we only have to validate our input once. We can do all the validation--cleaning up data from I/O, verifying it matches a certain shape, creating errors etc.--when we construct the instances of our types. That way all functions which accept those types are relieved from the obligation of checking themselves.


mypy supports generics. A generic can be a lot of things; A `list`, an `Iterable`, or something equivalent to scala/java 8's `Option` type. If a generic is a collection, all elements of the collection must be of the same type. mypy comes equipped with a number of generic types; take for example `List`, which is an alias for the built-in `list`.
```python 
ListOfInts = List[int]
```

You can also create types by subclassing `Generic`.
```python
class Option(Generic[T]):
    def getOrElse(t: T) -> T:
       . . . 
```
It's possible to use multiple type variables within a generic:
```python
E = TypeVar("E")
V = TypeVar("V")
class Either(Generic[E,V]):
    . . . . 
```

Let's use `List` and `3DPoint` to create a more complex product type: `Robot Legs`.

```python
RobotLegs = NamedTuple("RobotLegs", [("leftLeg", List[Point3D]), ("rightLeg", List[Point3D]), ("color", str)])
```
Note that we've defined the field `color` as simply a string, allowing us to create robot legs with nonsense colors. It's also possible to create robot legs with negative integers for coordinates! We only want pastel colors, and robots which exist in the cartesian plane. 
In fact it's possible to use this technique to *guarantee* that our function will only ever get valid input. It's only possible to construct the sum type of `RobotLegs` through the union type of `Color`; `Color` is by definition one of `Blue`, `Red`. . . and points
In languages with the concept of private constructors, it's possible to *guarantee* that a RobotLegs cannot be created an invalid state--and therefore that `getColor` can never be passed invalid data--by making the `RobotLegs` constructor private. Unfortunately, we can only document the `make3DCoordinates` function as the point of entry for our API--we can't exclude the constructor as private.

Note that the assurance offered by static typing is significantly stronger than the contract offered by ducked typing. If we simply accepted an object with `leftLeg` `rightLeg` and `color` as a RobotLeg, we'd have no guarantees that these fields were valid, or even that they were the expected type!

`Color` is a very simple Union type, analogous to the "Enums" of other languages (including python 3), while providing additional safety. Bution union types are more powerful; it's possible to create a union type out of product types, and model arbitrary complex 
systems this way. You can think of these types as representing the "set of all possible inputs and outputs" and functions accepting these types as representing the "cobminators" or "all the things I can ever do with my inputs". Together, these form a sort of "algebra" that represents your domain. In the domain of giant robots:

Great! we've created an API that's clear, self-documenting, and compartively safe. We've provided some limited guarantees of correctness;
and our domain is well-defined, which will help us reason about our past and future code moving forward.
mypy is a growing project; it's still in an early stage and being actively developed. It's become an official
part of they [python](github.com/python) flock as the definitive optional typechecker; it's got the [backing](https://github.com/python/mypy/issues/1276#issuecomment-192981427)
and [involvement](https://github.com/python/mypy/pull/1277) of [python's creator](https://en.wikipedia.org/wiki/Guido_van_Rossum).

Although mypy is still in active development, it can be a profitable tool right now. It's not a compiler, and it never touches
your code, so it can be used without much concern for bugs. It takes some extra time to annotate python with types--I've demonstrated
some of the strengths of its type inference, but it's necessary to annotate some things like lambda expressions, for example.
It's well worth the effort to document and verify your code in one way or another--mypy is another excellent tool for this purpose.
