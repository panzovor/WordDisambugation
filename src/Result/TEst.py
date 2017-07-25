__author__ = 'E440'

dicts = {"a":1,"b":2,"c" :3}
string ="aa"
keyset = ["a","b"]
for tmp in keyset:
    string+=tmp+ str(dicts[tmp])+","
print(string)