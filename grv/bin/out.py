from tetris import *

print ( 'Starting Tetris...' ) 
create_tetris__ ( 300  , 'Nimisha Tetris'  ) 
score = 0  
def get_score ( cleared  ) : 
	return cleared * ( 5 )  
	pass
 
run = True  
get_block__ ( ) 
while ( run  ) : 
	if ( block_fixed__ ( )  ) : 
		get_block__ ( ) 
		pass
 
	if ( lost_game__ ( )  ) : 
		run = False  
		end_game__ ( ) 
		break 
		pass
 
	event = get_inputs__ ( )  
	if ( event == 'QUIT'  ) : 
		run = False  
		end_game__ ( ) 
		break 
		pass
 
	elif ( event == 'K_LEFT'  ) : 
		move_left__ ( ) 
		pass
 
	elif ( event == 'K_RIGHT'  ) : 
		move_right__ ( ) 
		pass
 
	elif ( event == 'K_DOWN'  ) : 
		move_down__ ( ) 
		pass
 
	elif ( event == 'K_UP'  ) : 
		rotate__ ( ) 
		pass
 
	else : 
		pass
 
	render_game__ ( ) 
	pass
 
cleared = rows_cleared__ ( )  
score = get_score ( cleared )  
print ( 'Score: ' , score ) 
