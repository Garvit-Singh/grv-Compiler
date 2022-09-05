# .grv-Compiler (SoLo Project)
A Translator Compiler written in python and SLY which first converts ".grv" extension files into ".py" files then runs it using inbuilt libraries (*tetris.py as of now which aims to helps fast development of Customized Tetris Games*). Additionally shell to run code and try out syntax.  Automated Script will be provided in MAKE file. ( **Note**: Language is still under construction but this is sample code.) Compiler doesn't just aim to convert ".grv" to ".py" but also tries to handle both language compile errors as well as python conversion errors beforehand.
Compiler creates a single output file at a time, therefore, we can not run multiple files together since there will be only one copy of output file. Same goes for shell. Future updates will allow you to specify output file name which will help you manage the output files together yourselves.





# Compilation Process / Stages of compilation 
![Stages of Compilation](https://drive.google.com/uc?export=view&id=1sDQk0M-cWpvHkaNh_Mu1PHc-5Z4VVhXB)




# Commands 

### Installation Command
$ make install

### Compilation Command
$ make compile

Choose file to compile: filename.grv

### Command to run code
$ make run




# Unique Abstract Tree Design 
*A completely new design for abstract tree representation of a language has been bought about. This construction helped in converting code to python code tremendeously. Main Idea is to have a linked list for each statement at a particular nesting level while maintaining the syntax of our langauge and error checks. We create a new linked list for every nesting level introduced in code as an independent Abstract Tree for that subcode within that nesting.*
### Our Special Linked List Node
![Abstract Tree Node](https://drive.google.com/uc?export=view&id=1nP4XifUIF_DiQf_XICtR6goNdpiQHH5M)

### Our Abstract Syntax Tree **look-alike**
![Abstract Tree Representation](https://drive.google.com/uc?export=view&id=1b87zMRVHATy0JSgbgUMwKQM_jb13R6JB)



# Language Shell
(**Note**: This will take a line and override a pre-existing file which stores shell code, then run that file to do compile time check. We recommend using this for syntax checking. After running " *quit()* " in shell, shell will terminate and the latest copy of code will be ran for syntax checking.

### Command 
$ make shell

### Example Code
$ grv> console('Hello World!');
$ grv> quit()

### Preview 
![Shell Output](https://drive.google.com/uc?export=view&id=1gK_sg8DQp2DbXX3oiW8yL5f9YLfECQmZ)


# Language Syntax 
Language follows a mix of both C and Python. We do not need any variable types and at the same time langauge follows Block structure with curly braces and semicolons. 
Few example files are written showing how to use loops, function declaration and our inbuilt functions defined as *function_name__(..._)*. Language is ineffective of indentation instead uses semicolons and blocks as it's check points.


### Language Keywords : 
1. func 
2. return
3. if 
4. elif
5. else 
6. while
7. break
8. continue
9. console
10. '... string'

*Operators :* +, -, *, /, >, <, >=, <=, ==, !=, &&, ||, !




# Example Programs :

### Recursive Factorial :
    # Program for finding factorial of a numnber recursively
    func factorial(n) {
        if(n == 1) {
            return 1;
        }

        return n*factorial(n-1);
    }

    f = factorial(10);
    console('Factorial of 10 is: ', f);
    
 
 ### Tetris Program (using inbuilt functions) : 
 ![Tetris Output](https://drive.google.com/uc?export=view&id=1gi1wg11uzmdWS5dgQp31cIwO1MWwUGaA)
