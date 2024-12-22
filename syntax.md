# enlang Syntax Guide

## Variable Assignment

Use `is now` to assign a value to a variable:

```enlang
<variable_name> is now <value>
```

## Operators

- Addition: `plus`
- Subtraction: `minus`
- Multiplication: `times`
- Division: `divide`

Example:

```enlang
result is now a plus b
```

## Conditional Statements

Use `if` to start a conditional block:

```enlang
if <condition>
    <statements>
```

Conditions use `equals` for comparison:

```enlang
if x equals 10
    output "x is 10"
```

Use `else`if you want to do something when the condition is not true

```enlang
if x equals 10
    output "x is 10"
else
    output "x is not 10"
```

## Outputting Values

Use `output` to print to the console:

```enlang
output <value>
```

Example:

```enlang
output "Hello, World!"
```

## Using inputs to assign to a variable

```enlang
<variable_name> is now input
```

## Loops

Use `repeat x times` to create a loop that runs `x` times:

```enlang
repeat <number> times
    <statements>
```

Example:

```enlang
repeat 5 times
    output "Hello"
```
