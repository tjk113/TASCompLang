# TASCompLang
a small, extensible, declarative language for generating `Conditions.lua` files for use in [TAS-Comp-Bot](https://github.com/bxrru/TAS-Comp-Bot)'s Lua script timing system

[Read the guide to get started](https://github.com/tjk113/TASCompLang/blob/main/GUIDE.md)

## Example TCL file
```
course: ccm

start:
    action = "standing"

end:
    red_coin_count = 3
    action = "star dance ground (exits)"

require:
    action_count "triple jump" <= 2
    purple_switch_activated

ban:
    blj
```

## Available Game Info
Here is the game information that can be used in TCL files (format: `variable` 🡒 `return type`):  
- `action` 🡒 `string`
- `previous_action` 🡒 `string`
- `action_count "<action>"` 🡒 `number`  
The amount of times the specified action has been performed since timing began
- `animation` -> `string`
- `a_press_count` 🡒 `number`  
The amount of times A has been pressed since timing began (does not currently account for starting with A held)
- `purple_switch_activated` -> `boolean`  
Whether or not a purple switch is currently activated in the stage
- `yellow_box_broken_count` 🡒 `number`  
The amount of yellow boxes that have been broken since timing began (same idea for the other `<item>_box_broken_count` functions)
- `wing_box_broken_count` 🡒 `number`
- `metal_box_broken_count` 🡒 `number`
- `vanish_box_broken_count` 🡒 `number`
- `coin_count` 🡒 `number`
- `red_coin_count` 🡒 `number`
- `life_count` 🡒 `number`
- `mario_x` 🡒 `number`
- `mario_y` 🡒 `number`
- `mario_z` 🡒 `number`
- `mario_h_speed` 🡒 `number`
- `mario_wall_tri` -> `number`  
The memory address of Mario's currently referenced wall triangle
- `mario_floor_tri` 🡒 `number`  
The memory address of Mario's currently referenced floor triangle
- `mario_interact_object` 🡒 `number`  
The memory address of Mario's current iteraction object

## Bannable Strategies
Here are the strategies you can add to a `ban` section (\* = banned by default):    
- `blj`
- `c_up_slide`
- `downwarp`
- `goto_pu`*
- `use_warp`*
- `use_shell`
- `use_cannon`
- `leave_course`*
- `"[action]"`  
You can explicitly ban actions

## Available Functions
Here are the currently available standard functions (format: `function` 🡒 `return type`):
- `full_black_fadeout` 🡒 `boolean`  
Returns true on the first fully black frame of a fadeout

## Supported Operators
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal to
- `<=` Less than or equal to
- `=` Equal to
- `!=` Not equal to
