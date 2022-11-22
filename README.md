[![Build Status](https://app.travis-ci.com/Zatura/monstersgame-automation.svg?branch=master)](https://travis-ci.org/azu/travis-badge)

# monstersgame-automation

Containerized bot for game www.monstersgame.com.pt/  

## Login  
First, setup your secrets at credentials.py  
```python
bot = Bot()
scheduler = Scheduler()
scheduler.push(lambda: bot.login())
scheduler.execute()
```
  
## Daily hunt  
```python
scheduler.push(lambda: bot.hunt_humans())
scheduler.execute()
```
  
## Hunt random enemies
```python
scheduler.push(lambda: bot.hunt_enemies())
scheduler.execute()
```
Important: Attack criteria should be modified into hunt_enemies() function  

## Hunt the last 3 most wealthy recently attacked enemies  
```python
scheduler.push(lambda: bot.hunt_by_registry(3))
scheduler.execute()
```

## Work 5 hours at cemitery    
```python
scheduler.push(lambda: bot.work(5))
scheduler.execute()
```

## Enemies by list    
```python
scheduler.push(lambda: bot.hunt_by_list(known_enemies))
scheduler.execute()
```
known_enemies should be a list of strings into enemies.py

![image](https://user-images.githubusercontent.com/7329177/115079953-55877f80-9ed8-11eb-941e-57152824e4ae.png)

