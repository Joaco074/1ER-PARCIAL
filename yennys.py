class EmpleadoDeposito:
    def __init__(self, nombre, apellido, cargo, salario):
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.salario = salario

    def presentarse(self):
        return f"Me llamo {self.nombre} {self.apellido} y trabajo en el depósito de libros como {self.cargo}."

    


empleado1 = EmpleadoDeposito("Juan", "Pérez", "Bibliotecario", 30000)


print(empleado1.presentarse())

