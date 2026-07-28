# Block libraries

This submodule of the UI part of the package contains a few types of blocks for posterior use in UIs

    - dynamic_entries : Text entries with values being verified in them as well as a dynamizer object that can be added aas an attriubute to other objects to carry out that same task.

    - fancy_typing : introduces slight delays in text writting and deleting to make it look fancier

    - fonts : Wrappers for the default tkinter font functions

    - paired_widgets : Blocks made up of one or more widgets to make a functional widget as a whole

## dynamic entries

Simply signals to the user wether the value they are trying to input is valid or not, if the value is not valid the entry will remember and use the last valid entry it had to generate results, prevents dumb errors, signals visually when a field has an invalid input.

The dynamic entries are obsolete by way of the dynamizer class defined in the same library it is more flexible and can easily be adapted for other types of entries which are not text entries.
They do have an advantage as the valid entry protection is more solid and can prevent undue triggers with invalid data.

## fancy typing

just a fancy way for the machine to return results, gives it a better feel for the user.
to improve this i would need to make it so it doesn't write endline characters every time it stops writting i find that quite anoying

## fonts

boring wrapper

## paired wigets

Widget block that combine 2 or more widgets, this makes handling the grip or pack easier later on as objects that should always go together are already paired.
A convenient example would be the label and entry pair as you typically want these two to be paired to give info to the user it is already done for you and can be handled as a single block.