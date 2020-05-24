# monstersgame-automation
## Login  
First, setup your secrets at credentials.py  
`bot = Bot()`  
`scheduler = Scheduler()`  
`scheduler.enqueue(bot.login)`  
`scheduler.execute()`  
  
## Daily hunt  
`scheduler.enqueue(bot.hunt_humans)`  
`scheduler.execute()`
  
## Hunt random enemies
`scheduler.enqueue(bot.hunt_enemies)`  
`scheduler.execute()`
Attention: Attack criteria should be modified into hunt_enemies() function  
  
## Enemies by list    
`scheduler.enqueue(lambda: bot.hunt_by_list(known_enemies))`  
`scheduler.execute()`  
known_enemies should be a list of strings into enemies.py


