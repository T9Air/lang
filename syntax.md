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

## Valid Conditions

The following conditions can be used in both `if` statements and `repeat until` loops:

- `=` - checks if two values are equal
- `!=` - checks if two values are not equal
- `>` - checks if first value is greater than second value
- `<` - checks if first value is less than second value
- `>=` or `=>` - check if the first value is greater than or equal to the second value
- `<=` or `=<` - check if the first value is less than or equal to the second value

## Conditional Statements

Use `if` to start a conditional block, using any valid condition from the list above:

```enlang
if <condition>
    <statements>
```

Example:

```enlang
if x = 10
    output "x is 10"
```

Use `else` if you want to do something when the condition is not true

```enlang
if x = 10
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

### Running a block of code x amount of times

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

### Running a block of code until a certain condition is met

Use `repeat until` to create a while loop that runs until any valid condition from the list above is met:

```enlang
repeat until <condition>
    <statements>
```

Examples using different conditions:

```enlang
repeat until count = 10
    output count
    count is now count plus 1

repeat until temperature > 100
    temperature is now temperature plus 5
```
