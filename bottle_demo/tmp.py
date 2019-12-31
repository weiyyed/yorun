var = "This is a string"
varName = 'var'
s= locals()[varName]
s2=vars()[varName]

print (s)
print (s2)
print (eval(varName))