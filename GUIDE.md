# TASCompLang Guide
## <a name="basic-structure"></a>Basic Structure
The bare minimum TCL file looks something like this:
```
course: bob

start:
    action = "standing"

end:
    action = "star dance ground (exits)"
```
Each section is declared with a label and a colon. All sections except for `course` also require at least one newline after the section label (see: [Course Specification](#course-specification)). All TCL files must have `course`, `start`, and `end` sections.  

The `start` and `end` sections are where you provide the conditions for when timing should start and end, respectively. Each condition must be separated by at least one newline. Timing will start once every condition in the `start` section is true, and timing will end once every condition in the `end` condition is true.

**IMPORTANT**: The last condition in the `end` section is assumed to be the condition upon which timing should *actually* end. For example, if your end section looks like this:
```
end:
    red_coin_count <= 3
    action = "star dance ground (exits)"
```
then `red_coin_count <= 3` is only checked *after* `action = "star dance ground (exits)"` is true. This way, if Mario collects the star but doesn't get 3 or more red coins, then a proper DQ message can be generated (see: [Disqualification](#disqualification)).

Capitalization is ignored, except for custom function names (see: [Custom Functions](#custom-functions)), all unnecessary whitespace is ignored, and comments may be written after a `//` prefix.

## <a name="optional-sections"></a>Optional Sections
In addition to the required sections, there are three optional sections that may also be provided:
```
require:
    life_count < 1

ban:
    blj
    "triple jump"

allow:
    leave_course
```
The conditions in a `require` section must be true on every frame during timing. Each condition must be separated by at least one newline. A `ban` section lets you ban particular strategies or actions from your task (see: [List of supported strategies and actions](https://github.com/tjk113/TASCompLang/blob/main/strats_list.py)). Each strategy/action must be separated by at least one newline.  

There are three strategies which are banned by default: `leave_course`, `use_warp`, and `goto_pu`. An `allow` section can be used to explicitly allow any of these 3 strategies. 

## <a name="disqualification"></a>Disqualification
Disqualifications, or "DQs", are handled automatically for everything except custom functions. DQs from custom functions should be handled from within the functions by calling `DQ("<message>")` wherever a DQ should occur.

## <a name="custom-functions"></a>Custom Functions
Some tasks may be too complex to describe using only the default functionality of TCL. You therefore have the option to integrate your own custom Lua functions. In the `start`, `end`, and `require` sections, you have access to any global functions you've written in a custom functions file.  

Your functions may only return a boolean, number, or string, as these are the only representable data types in TCL. The name of the function you use in the TCL file must match the name and case of the function's signature in your custom functions file.

To enable custom functions, use the `-cf` compiler flag. The compiler will look for `CustomFunctions.lua` in the current directory by default, but you may optionally provide an file path (see: [Compiler Usage](#compiler-usage)).

For information about custom functions and DQing, see [Disqualification](#disqualification).

## <a name="course-specification"></a>Course Specification
Courses should be specified by initials or full name:
```
course: ttm
```
```
course: Tall, Tall Mountain
```
It is recommended to use course initials, because if you specify a course by full name you must use proper spelling and punctation. Captialization, however, is not required with either method (`course: ttm` is the same as `course: TTM`).  

You may also to specify a course by its stage index, but this is less intuitive, as many courses' internal stage indices don't match their in-game course numbers. The primary use of this should be for tasks that take place in romhacks.  

A newline is not required for this section, given that it only has one necessary line. You can still use as many as you'd like, though.

## <a name="compiler-usage"></a>Compiler Usage
Help Menu:
```
usage: tcl.py [-h] [-cf [CF]] [-o O] src

positional arguments:
  src         TASCompLang source file

options:
  -h, --help  show this help message and exit
  -cf [CF]    use custom functions (provide a path to override the default "CustomFunctions.lua")
  -o O        path to output file
```
Example:
```
$ python tcl.py task1.tcl -cf task1customfuncs.lua -o TimingLua/Conditions.lua
                ^ src file    ^ optional cf path      ^ optional output path
```
By default, the compiler outputs a file named `Conditions.lua` in the current directory, but you may optionally provide another output path using the `-o` flag.

If your TCL file uses custom functions (see: [Custom Functions](#custom-functions)), then you must use the `-cf` compiler flag. If you don't provide a path to this flag, the compiler will look for a file named `CustomFunctions.lua` in the current directory.

After you have you've generated your `Conditions.lua` file, make sure it's in the bot's `TimingLua` directory. Then you'll be ready to start timing submissions 😀.
