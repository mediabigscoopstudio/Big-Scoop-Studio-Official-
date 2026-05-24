from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'main.urls', name='main'),  
    host(r'master', 'master.urls', name='master'), 
    host(r'manager', 'manager.urls', name='manager'), 
    host(r'teams', 'teams.urls', name='teams'), 
    host(r'clients', 'clients.urls', name='clients'), 

)