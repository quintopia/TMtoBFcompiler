# TMtoBFcompiler
Compiles Turing Machines to Brainfuck

Uses Scanner.py from [this project](https://github.com/florton/Turing-Machine-Compiler) and which means it reads Turing machines in the same syntax and provides most of the same features. The script is not duplicated here because no licensing information is provided, but you can just drop the file into the same folder and it will work.

Note that the generated programs will not append a "#" to their inputs the way Lorton's TuringMachine.py does. If you use one of the example TMs from that page, you will need to add the # to your inputs yourself.

Call it like `python2 BFCompile.py machine3.tm > machine3.b`.
