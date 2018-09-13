

def lammpscluster(lmp, obj):
    coords = obj.getfeature()

    lmp.command("clear")
    lmp.command("region simbox box -100 100 -100 100 -100 100")
    lmp.command("create_box 1 simbox")


