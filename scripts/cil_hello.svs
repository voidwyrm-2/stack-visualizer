@useVars
@vars 1
@useLine
@useOutput

wait

// string text = "This is a string!";
line "ldstr \"This is a string!\""
push.s "This is a string!"

wait

line "stloc.0"
pop.0

wait

// Console.WriteLine("Hello, Catdog!");
line "ldstr \"Hello, Catdog!\""
push.s "Hello, Catdog!"

wait

line "call void [System.Console]System.Console::WriteLine(string)"
pop.o

wait

// Console.WriteLine(text);
line "ldloc.0"
push.0

wait

line "call void [System.Console]System.Console::WriteLine(string)"
pop.o

wait

// text += " This is an addition to the string!";
line "ldloc.0"
push.0

wait

line "ldstr \" This is an addition to the string!\""
push.s " This is an addition to the string!"

wait

line "call string [System.Runtime]System.String::Concat(string, string)"
pop.n
pop.n
push.s "This is a string! This is an addition to the string!"

wait

line "stloc.0"
pop.0

wait

// Console.WriteLine(text);
line "ldloc.0"
push.0

wait

line "call void [System.Console]System.Console::WriteLine(string)"
pop.o