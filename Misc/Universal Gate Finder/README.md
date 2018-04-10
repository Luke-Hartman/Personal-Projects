# Universal Gate Finder

This program tries to find all the gates with n inputs and 1 outputs that are universal.
(Made while taking CS352 Digital Systems Fundamentals)

A universal gate is a gate which can implement all logic functions. (Examples are NAND, NOR, perceptrons, etc.)

It is sufficient to show that a gate implements NOT and (AND or OR) to show that it is universal.

Notation for a 2 input gate is Gate1 = {[input 1]-[input 2]-> [Gate2] <=> {Truth Table}}

(You get Gate1 by putting [input 1]-[input 2] into [Gate2])

Gate2 can also use the same nested notation.


X is the universal gate that was found.

A, B are the inputs for the truth table {AB A~B ~AB ~A~B}

1, 0 are true, false hard wired inputs.


## Example Output for n=2:
Found universal gate:
F F F T 


This is either AND or OR
{[A]-[X]-> [{[B]-[B]-> [X] <=> { F T F T }}] <=> { T T T F }}

This is NOT
{[A]-[A]-> [X] <=> { F F T T }}


Found universal gate:
F F T F 


This is either AND or OR
{[A]-[{[B]-[A]-> [X] <=> { F T F F }}]-> [{[B]-[A]-> [X] <=> { F T F F }}] <=> { T F F F }}

This is NOT
{[A]-[1]-> [X] <=> { F F T T }}


Found universal gate:
F T F F 


This is either AND or OR
{[A]-[X]-> [X] <=> { T F F F }}

This is NOT
{[1]-[A]-> [X] <=> { F F T T }}


Found universal gate:
F T T T 


This is either AND or OR
{[A]-[X]-> [{[B]-[B]-> [X] <=> { F T F T }}] <=> { T F F F }}

This is NOT
{[A]-[A]-> [X] <=> { F F T T }}


Found universal gate:
T F T T 


This is either AND or OR
{[A]-[{[B]-[A]-> [X] <=> { T T F T }}]-> [{[B]-[A]-> [X] <=> { T T F T }}] <=> { T T T F }}

This is NOT
{[A]-[0]-> [X] <=> { F F T T }}


Found universal gate:
T T F T 


This is either AND or OR
{[A]-[X]-> [X] <=> { T T T F }}

This is NOT
{[0]-[A]-> [X] <=> { F F T T }}