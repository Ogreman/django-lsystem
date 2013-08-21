django-lsystem
==============

Prototype python implementation of a [Lindenmayer system](https://en.wikipedia.org/wiki/L-system) that uses Django as a backend for storing generated data.

Very much a WIP and not intended for serious use.


Example tree:
-------------

  Start: X
  Theta: 25.7
  Move: 5.0

  X -> F[+X][-X]FX

  F -> FF

