# TMtoBFcompiler
Compiles Turing Machines to Brainfuck

Uses Scanner.py from [this project](https://github.com/florton/Turing-Machine-Compiler) and which means it reads Turing machines in the same syntax and provides most of the same features. The script is not duplicated here because no licensing information is provided, but you can just drop the file into the same folder and it will work.

Note that the generated programs will not append a "#" to their inputs the way Lorton's TuringMachine.py does. If you use one of the example TMs from that page, you will need to add the # to your inputs yourself. Likewise, rather than outputting the tape up to a "#" character, like TuringMachine.py, using Output() with unspecified endpoint will output the tape up to the first blank (zero). You can embed null bytes into your Turing machines to handle blanks, or you can use another symbol and put it on the ends of all your inputs like Lorton.

Call it like `python2 BFCompile.py machine3.tm > machine3.b`.
