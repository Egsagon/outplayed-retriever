'''
    Outplayed retriever
    
    Allows to retrieve pathes from favorites
    outplayed replays.
    
    https://github.com/Egsagon/outplayed-retriever
'''

import os
import json
from time import time
from sys import getsizeof

print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
print('┃ \033[7m Outplayed paths retriever\033[0m ┃')
print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

ps1 = '\033[92m*\033[0m'
start = time()

# Fetch Outplayed directory
print(ps1, 'Fetching data...')
app = os.path.expanduser('~') + '/AppData/Roaming/Overwolf/'
dirs = os.listdir(app)

# Fetch backup file
assert len(dirs) == 1
target = app + dirs[0]
backups = [f for f in os.listdir(target) if f.startswith('backup')]
backup = target + '/' + sorted(backups)[-1]
print(ps1, 'Using backup at\033[92m', target, '\033[0m')

# Parse data
print(ps1, 'Parsing backup...')
data = json.load(open(backup))
data = {k: v for k, v in data.items() if 'MATCH' in k}
print(ps1, f'Parsed \033[92m{getsizeof(data)}\033[0m octets of backups')

# Extract paths
paths = []
length = len(data)
print(ps1, f'Fetched \033[92m{length}\033[0m entries.')

game = 'Outplayed\\' + input(ps1 + ' Enter game name: ').title()

print(ps1, f'Filtering pathes with \033[92m{game}\033[0m')

for i, (uuid, match) in enumerate(data.items()):
    
    print('\r' + ps1, f'Iterating: \033[91m{i + 1}\033[0m/{length}', end = '')
    
    match_data = json.loads(match)
    medias = match_data.get('medias')
    
    if not medias: continue
    
    for media in medias:
        if media.get('isFavorite') and (path := media.get('path')):
            
            if not game in media.get('path', ''): continue
            
            paths += [path]

# Save to file
end_parsing = time()
length = len(paths)
print('\n' + ps1, f'Fetched \033[92m{length}\033[0m replays!')
output = input(ps1 + ' Enter output file (default=output.txt): ') or 'output.txt'

start_writing = time()

with open(output, 'w') as f:
    
    for i, url in enumerate(paths):
        print('\r' + ps1, f'Writing: \033[91m{i + 1}\033[0m/{length}', end = '')
        
        f.write(url + '\n')

final_time = time() - start_writing + end_parsing - start
print('\n' + ps1, f'Done in \033[93m{round(final_time, 3)}\033[0ms.')

# EOF