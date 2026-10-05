#smart app 1
#Esper

#functies

def aantal_dagen(inputFile):
    aantal = 0
    txt = open(inputFile)
    txt.readline()

    for i in txt:
        aantal += 1

    txt.close()
    return aantal


def auto_bereken(inputFile, outputFile):
    txt = open(inputFile)
    txt_dumb = open(outputFile, "w")

    txt.readline()

    for regel in txt:
        data = regel.split()

        date = data[0]
        numPeople = int(data[1])
        tempSetpoint = float(data[2])
        tempOutside = float(data[3])
        precip = float(data[4])

        verschil = tempSetpoint - tempOutside

        if verschil >= 20:
            cv = 100
        elif verschil >= 10:
            cv = 50
        else:
            cv = 0

        ventilatie = min(numPeople + 1, 4)
        bewatering = precip < 3

        txt_dumb.write(f"{date};{cv};{ventilatie};{bewatering}\n")

    txt.close()
    txt_dumb.close()


def overwrite_settings(outputFile):
    datum = input("Welke datum wil je aanpassen? voorbeeld: 08-10-2024 \n> ")

    try:
        systeem = int(input("Welk systeem? (1 = CV ketel, 2 = ventilatie, 3 = bewatering). \n> "))
        waarde = int(input("Welke waarde? \n> "))
    except ValueError:
        return -3

    if systeem not in [1, 2, 3]:
        return -3

    if systeem == 1 and (waarde < 0 or waarde > 100):
        return -3

    if systeem == 2 and (waarde < 0 or waarde > 4):
        return -3

    if systeem == 3 and waarde not in [0, 1]:
        return -3

    txt = open(outputFile, "r")
    regels = txt.readlines()
    txt.close()

    gevonden = False
    nieuwe_regels = []

    for i in regels:
        data = i.strip().split(";")

        if data[0] == datum:
            gevonden = True

            if systeem == 1:
                data[1] = str(waarde)

            elif systeem == 2:
                data[2] = str(waarde)

            elif systeem == 3:
                if waarde == 0:
                    data[3] = "False"
                else:
                    data[3] = "True"

            i = ";".join(data) + "\n"

        nieuwe_regels.append(i)

    if not gevonden:
        return -1

    txt = open(outputFile, "w")
    txt.writelines(nieuwe_regels)
    txt.close()

    return 0


def smart_app_controller():

    while True:
        print()
        print("SMART APP CONTROLLER")
        print("====================")
        print("1. Hoeveel dagen zijn er aanwezig?")
        print("2. Autobereken alle actuatoren")
        print("3. Overschrijf een berekende waarde")
        print("4. Stoppen")

        try:
            keuze = int(input("> "))
        except ValueError:
            print("Ongeldige keuze, probeer opnieuw.")
            continue

        if keuze == 1:
            print("Aantal dagen:", aantal_dagen("vars.txt"))

        elif keuze == 2:
            auto_bereken("vars.txt", "output.txt")
            print("Actuatoren succesvol berekend en opgeslagen in output.txt.")

        elif keuze == 3:
            resultaat = overwrite_settings("output.txt")

            if resultaat == 0:
                print("Waarde succesvol aangepast.")
            elif resultaat == -1:
                print("Datum niet gevonden.")
            elif resultaat == -3:
                print("Ongeldige invoer.")

        elif keuze == 4:
            print("Programma gestopt.")
            break

        else:
            print(f"keuze '{keuze}' is geen keuze, probeer opnieuw.")


# main loop
smart_app_controller()
