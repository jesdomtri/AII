# encoding: utf-8
from locale import str


class Cadena:

    def __init__( self ):
        print( "=== Cadenas ===" )
        print ( self.e1_a( 'separar', ',' ) )
        print ( self.e1_b( 'mi archivo de texto.txt', '_' ) )
        print ( self.e1_c( 'su clave es: 1540', 'X' ) )
        print ( self.e1_d( '2552552550', '.' ) )
        print ( self.e2_a( 'subcadena', 'cadena' ) )
        print ( self.e2_b( 'kde', 'gnome' ) )
        print( '\n' )

    def e1_a( self, s, c ):
        return c.join( list( s ) )

    def e1_b( self, s, c ):
        return s.replace( " ", c )

    def e1_c( self, s, c ):
        l = list( s )
        res = []
        for i in l:
            if i in '0123456789':
                res.append( c )
            else:
                res.append( i )
        return ''.join( res )

    def e1_d( self, s, c ):
        resultado = []
        contador = 0
        for caracter in list( s ):
            if contador == 3:
                resultado.append( '.' )
                contador = 0
            resultado.append( caracter )
            contador += 1
        return "".join( resultado )

    def e2_a( self, s1, s2 ):
        return s2 in s1

    def e2_b( self, s1, s2 ):
        return s1 if s1 < s2 else s2


class Tuplas:

    def __init__( self ):
        print( '=== Tuplas ===' )
        self.e1_a( ( 'Luis', 'Marta', 'Paula' ) )
        self.e1_b( ( 'Luis', 'Marta', 'Paula', 'Luis' ), 1, 3 )
        self.e1_c( ( ( 'Luis', 'h' ), ( 'Marta', 'm' ), ( 'Paula', 'm' ) ) )
        print ( self.e2( ( ( 'Garcia', 'Luis', 'M' ), ( 'Carrillo', 'Marta', 'J' ), ( 'Fernandez', 'Paula', 'M' ) ) ) )
        print( '\n' )

    def e1_a( self, nombres ):
        for i in nombres:
            print( 'Estimado', i, ', vote por mi' )

    def e1_b( self, nombres, p, n ):
        for i in nombres[p:n]:
            print( 'Estimado', i, ', vote por mi' )

    def e1_c( self, nombres ):
        for i in nombres:
            if i[1] == 'h':
                print( 'Estimado', i[0], ', vote por mi' )
            else:
                print( 'Estimada', i[0], ', vote por mi' )

    def e2( self, nombres ):
        res = []
        for i in nombres:
            nombre = ''.join( i[1] + ' ' + i[2] + '.' + ' ' + i[0] )
            res.append( nombre )
        return res


class Busqueda:

    def __init__( self ):
        print( '=== Busqueda ===' )
        print ( self.e1( [( 'Jorge Garcia', '12345' ), ( 'Luisa Montero', '54321' ), ( 'Ines Roca Diaz', '67890' )], 'Garcia' ) )
        print( '\n' )

    def e1( self, l, c ):
        res = []
        for tupla in l:
            for atributo in tupla:
                if c in atributo:
                    res.append( tupla )
        return res


class Diccionario:

    def __init__( self ):
        print( '=== Diccionario ===' )
        self.e1( {'Jorge':'12345', 'Luisa':'54321', 'Marta':'67890'} )
        print( '\n' )

    def e1( self, d ):
        while True:
            nombre = input( 'Introduzca un nombre: ' )
            if nombre == '*':
                break
            if nombre in d:
                print ( 'Telefono: ', d[nombre] )
                respuesta = input( 'Es correcto? (s/n): ' )
                if respuesta == 'n':
                    telefono = input( 'Introduzca el nuevo telefono: ' )
                    d[nombre] = telefono
            else:
                print( 'Este nombre no existe' )
                telefono = input( 'Introduzca telefono para crear a este usuario: ' )
                d[nombre] = telefono
        print ( d )


class Corcho:

    def __init__( self, nombre ):
        self.bodega = nombre


class Botella:

    def __init__( self, corcho ):
        self.corcho = corcho
        print ( 'Botella de la bodega ' + corcho.bodega )


class Sacacorchos:

    def __init__( self ):
        self.corcho = None

    def destapar( self, botella ):
        print( 'Destapando...' )
        self.corcho = botella.corcho
        botella.corcho = None

    def limpiar( self ):
        print( 'Limpiando...' )
        self.corcho = None


class Objeto:

    def __init__( self ):
        print( '=== Objeto ===' )
        corcho = Corcho( 'Micasa' )
        botella = Botella( corcho )
        sacacorcho = Sacacorchos()
        sacacorcho.destapar( botella )
        sacacorcho.limpiar()
        print( '\n' )


class Personaje:

    def __init__( self ):
        self.vida = 100
        self.posicion = {"Norte":0, "Sur":0, "Este":0, "Oeste":0}
        self.velocidad = 1

    def recibirAtaque( self, danyoRecibido ):
        print( 'Has recibido ' + str( danyoRecibido ) )
        self.vida -= danyoRecibido
        if self.vida <= 0:
            print( 'Has muerto' )
        else:
            print( 'Te queda ' + str( self.vida ) + ' de vida' )

    def mover( self, p ):
        self.posicion[p] += self.velocidad


class Soldado( Personaje ):

    def __init__( self ):
        Personaje.__init__( self )
        self.ataque = 3

    def atacar( self, objetivo ):
        objetivo.recibirAtaque( self.ataque )


class Campesino( Personaje ):

    def __init__( self ):
        Personaje.__init__( self )
        self.cosecha = 1

    def cosechar( self ):
        return self.cosecha


class Herencia:

    def __init__( self ):
        print( '=== Herencia ===' )
        soldado = Soldado()
        campesino = Campesino()
        soldado.atacar( campesino )
        soldado.atacar( campesino )
        print( 'Has cosechado ' + str( campesino.cosechar() ) )


if __name__ == "__main__":
    cadena = Cadena()
    tuplas = Tuplas()
    busqueda = Busqueda()
    diccionario = Diccionario()
    objeto = Objeto()
    herencia = Herencia()
