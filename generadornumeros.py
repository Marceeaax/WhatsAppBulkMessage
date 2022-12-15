# create an empty list
lista = []

# create a loop that creates a string from 595971 to 595976
for i in range(595971, 595976):
    # create a string from the number
    numero = str(i)
    # create a loop that goes from a string 000000 to 999999

    for j in range(0, 1000000):
        numerofinal = numero + str('{0:06}'.format(j))
        # append the number to the list
        lista.append(numerofinal)
        print(numerofinal)
        #print a newline                                                                                                





