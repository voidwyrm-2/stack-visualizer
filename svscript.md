# SVScript
The scripting language I made to control stack visualizations<br>
It has a simple syntax based on Common Intermediate Language(CIL), which is what C# compiles into

For examples, see the [scripts](./scripts) folder

# Commands/Instructions
Name | Description
---- | -----------
`nop` | Does nothing
`exit` | Stops the visualization at that point
`wait` | Waits for spacebar to be pressed
`push.[op] [argument]` | Pushes something to the stack
`pop.[op]` | Pops something off the stack
`line [argument]` | Sets the line to a string literal

**Push Operators**
Name | Description
---- | -----------
`s` | Pushes the given string literal to the stack
`n` | Pushes the given number literal to the stack
`b` | Pushes the given boolean literal to the stack
`[number]` | Pushes the variable of that index to the stack

**Pop Operators**
Name | Description
---- | -----------
`n` | Pops a value off the stack and does nothing with it
`o` | Pops a value off the stack and sets the output to it
`[number]` | Pops a value off the stack and sets the variable of that index to it

**Directives**<br>
Directives are used for flagging certain things
Directive | Description
--------- | -----------
`@useVars` | Turns on showing the variables(added for emulation of CIL's local variables)
`@vars [count]` | Says how many variables there are(added for emulation of CIL's local variables)
`@useLine` | Turns on showing the code line, which can be used for showing a snippet of code
`@useOutput` | Turns on showing the output, which is used for emulation of a text output, such as the console