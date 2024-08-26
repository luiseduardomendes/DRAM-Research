with open("input.dat", "w") as f:
  
  for i in range(64):
    if i > 23 and i < 29:
      tmp = 256
    else:
      tmp = 0

    f.write( f"{tmp}\n" )