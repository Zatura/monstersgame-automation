# monstersgame-automation
## Login  
First, setup your secrets at credentials.py  
`bot = Bot()`  
`scheduler = Scheduler()`  
`scheduler.push(lambda: bot.login())`  
`scheduler.execute()`  
  
## Daily hunt  
`scheduler.push(lambda: bot.hunt_humans())`  
`scheduler.execute()`
  
## Hunt random enemies
`scheduler.push(lambda: bot.hunt_enemies())`  
`scheduler.execute()`  
Attention: Attack criteria should be modified into hunt_enemies() function  

## Hunt the last 3 most wealthy enemies recently attacked   
`scheduler.push(lambda: bot.hunt_by_registry(3))`  
`scheduler.execute()`  

## Work 5 hours at cemitery    
`scheduler.push(lambda: bot.work(5))`  
`scheduler.execute()`  

## Enemies by list    
`scheduler.push(lambda: bot.hunt_by_list(known_enemies))`  
`scheduler.execute()`  
known_enemies should be a list of strings into enemies.py


