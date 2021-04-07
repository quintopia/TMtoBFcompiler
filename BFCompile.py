from Scanner import Scan
import sys

def BFCompile(machine):
    functions = machine[3]
    
    #read input onto tape
    output = ">>>>,[>>>,]<<<[<<<]>>"
    
    #initial start state
    for i,state in enumerate(machine[2]):
        if machine[2][state]["start"]:
            output += "+"*(i+1)
            break

    #start main loop
    output += "["
    
    #insert breakpoint if debug is on (printing all the info TuringMachine prints for debug would greatly expand the length of programs)
    if functions['debug']:
        output+="#~@"
    
    #move state, set up state detection flag
    output += "[<+>-]>>+<<<"
    
    #insert switch case block for states
    output += GenerateStateMachine(machine[2],0,functions['rejectEdges'])
    
    #end main loop (going one TM cell back because pointer will be one TM cell right of where it actually should be)
    output += "<<]>"
    
    #output result
    if machine[1] is not None:
        start=0
        final=''
        if machine[1][0]:
            start = machine[1][0]
        if machine[1][1]:
            final = machine[1][1]
        if functions['pipe']:
            output+="["
        
        if final=="":
            output += "[>+<-]>>>[.>>>]<<<[<<<]>[<+>-]<<"+"+"*10+".>"
        else:
            output += ">>>"*(1+start)+".>>>"*(final-start)+"<<<"*(1+final)+"<"+"+"*10+".>"
        if functions['pipe']:
            output+=">]+[<"+"+"*88+".>->"+"+"*10+".[-]]<"
    
    #output accept(1) or reject(0) on next line
    output += "+"*48+"."
    
    #append input
    output+="!"+machine[0]
    
    #remove useless moves
    while "><" in output or "<>" in output or "-+" in output:
        output = output.replace("><","")
        output = output.replace("<>","")
        output = output.replace("-+","")

    return output

#enters on temp, leaves on temp
def GenerateStateMachine(states,idx,rejectEdges):
    #base case: we're out of states. assume reject state. (-2 in first cell)
    if idx>=len(states):
        #Neither Scanner.py nor TuringMachine.py seem to check for transitions to nonexistent states. ¯\_(ツ)_/¯
        return "<<+[<<<]>>>[-]>>"
    
    #get key for state
    key = list(states.keys())[idx]
    
    #is this the current state?
    output="-["
    
    #if not, try next state
    output += GenerateStateMachine(states,idx+1,rejectEdges)
    
    #if one of lower-valued states has not run, flag is set: test it
    output += "]>>>["
    
    #if this is a halt state, go to beginning of tape and set flag
    if states[key]["modifier"] is not None:
        output+="-<<+[<<<]>"+ "+"*(states[key]["modifier"]=="accept") + ">>[-]"
    else:
        #otherwise, handle transitions
        #copy symbol to state cell
        output += "<[<+>-]<"
        
        #insert transition function switch case
        output += HandleTransition(states,key,0,0,rejectEdges)

    #exit conditional and return to temp
    output += ">>]<<<"
    
    return output



#enters on state cell, leaves on NEXT state cell
def HandleTransition(states,statekey,transitionidx,lastsymbol,rejectEdges):
    #get next symbol
    try:
        symbol = sorted(states[statekey]["edges"].keys())[transitionidx]
    except:
        #base case: transition does not exist. go to reject state
        if rejectEdges:
            return "[<<<]>>>[-]"
        else:
            return "#~@missing edge" # and ~ and @ have been used as breakpoint symbols
    
    #check if this symbol is the one on the tape
    output="-"*(ord(symbol)-lastsymbol)+"["
    
    #if not, try next symbol
    output += HandleTransition(states,statekey,transitionidx+1,ord(symbol),rejectEdges)
                               
    #check that another transition has not already been performed
    output += "]>>[-<"
    
    #get transition
    transition = states[statekey]["edges"][symbol]
    
    #write symbol
    output+="+"*ord(transition[0])
    
    #move to next tape cell
    if transition[1]=="L":
        #state and temp should already be clear, so just move to next state left and clear
        output+="<<<<-"
    elif transition[1]=="R":
        #make sure state cell is set, then move to next state right
        output+="<+>>>"
    else:
        #just move to state for this cell
        output+="<"
    
    #write new state
    output+="+"
    for state in states.keys():
        if state==transition[2]:
            break
        output+="+"
    else:
        print("There is no "+transition[2]+" state (transition from "+state["name"]+")")
        sys.exit(1)
    
    
    #go to next next temp to close conditional, return to next state cell
    output += ">>>>>]<<"
    
    return output
    
if __name__=="__main__":
    try:
        print(BFCompile(Scan(sys.argv[1])))
    except:
        raise RuntimeError("Please specify a valid turing language file")
