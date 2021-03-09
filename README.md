# python turing machine

turing machine by python.

## usage

```
python machine.py sequence orderFile
```

### example

```
python mahcine.py 1101011 parindrome.txt
```

## orderFile format

One order must have 5 elements.

1. current state
1. character of tape
1. character that head will print
1. move direction (L: Left R: Right S: Stay)
1. transition state

### example

```
s0,0,0,L,s1
```

That means 

```
When state of machine is 's0' and character that machine read is '0', print'0', move left, and trans to state 's1'.
```

### note

- There should be no space after the comma. The machine will not ignore the spaces.
- The machine cannot print comma because it is delimiter.