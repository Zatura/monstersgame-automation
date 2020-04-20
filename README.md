# monstersgame-automation
## Login  
First, setup your secrets at credentials.py
`bot = FarmerBot()`  
`bot.login()`  
  
## Daily hunt  
`bot.hunt_humans()`  
  
## Hunt random enemies
`bot.hunt_enemies()`  
Attention: Attack criteria should be modified into hunt_enemies() function  
  
## Enemies by list    
`bot.hunt_by_list(known_enemies)`  
known_enemies should be a list of strings into enemies.py


