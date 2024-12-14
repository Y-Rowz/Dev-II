import math

class Fraction:
    """Class representing a fraction and operations on it

    Author : Loan ISTAS
    Date : Novembre 2024
    This class allows fraction manipulations through several operations.
    """

    def __init__(self, num: int =0 , den: int=1):
        """This builds a fraction based on some numerator and denominator.

        PRE :   inisalise  self.numerateur et self.numerateur:
                    -num (int): numérateur de de la fraction et ne peut etre égal à 0
                    -den (int):dénuminateur de tout les calculs
        POST :  Si den n'est pas nul, une nouvelle fraction est construite et la fraction simplifiée est également créée.
                Si à la fois den et num sont négatifs, ils sont rendus positifs selon les propriétés des fractions.
                Les self.__den et self.__num sont privé.
                Toutes les variables de la class Fraction sont immuable.
                ex Fraction(10,5):
                    - self.__num = 10
                    - self.__den = 5
                    - self._simNum = 2
                    - self._simDen = 1
        RAISE : ZeroDivisionError => le dénominateur ne peut pas etre égal à 0
        """

        if den == 0 :
            raise ZeroDivisionError

        if num >= 0 and den >= 0:
            self.__num = num
            self.__den = den
        elif den < 0 <= num:
            #garde le négatif du côter numérateur
            self.__num = -num
            self.__den = -den
        elif num < 0 < den:
            # garde le négatif du côter numérateur
            self.__num = num
            self.__den = den
        else :
            #si le num et den sont négatif, on met les deux en positif
            self.__num = abs(num)
            self.__den = abs(den)

        gcd = math.gcd(int(self.__num), int(self.__den))
        self._simNum = self.__num/gcd
        self._simDen = self.__den/gcd
        pass

    @property
    def numerator(self):
        """retourne le numerateur

        PRE : /
        POST : retourne le numérateur
        """
        return self.__num
    @property
    def denominator(self):
        """retourne le denominateur

        PRE : /
        POST : retourne le denominateur
        """
        return self.__den

    @property
    def numerator_simplifiee (self):
        """retourne la version simplifiée du numerateur

        PRE : /
        POST : retourne le numérateur
        """
        return self._simNum
    @property
    def denominator_simplifiee (self):
        """retourne la version simplifiée du denominateur

        PRE : /
        POST : retourne the denominateur (int)
        """
        return self._simDen


# ------------------ Textual representations ------------------

    def __str__(self) :
        """Return a textual representation of the reduced form of the fraction

        PRE : /
        POST : Retourne une représentation textuelle de la fraction réduite.
            exemple :
                - fraction(10,5) => 2/1

        """
        return f'{self._simNum}/{self._simDen}'

    def as_mixed_number(self) :
        """Return a textual representation of the reduced form of the fraction as a mixed number
        A mixed number is the sum of an integer and a proper fraction

        PRE : /
        POST : Retourne une représentation textuelle de la fraction réduite sous la forme d'un nombre entier et de son reste.
            exemple :
                - fraction(10,5) => 2 + 0/1
                - fraction(11,5) => 2 + 1/5
                - fraction(-11,5) => -3 + 4/5
        """
        integer = math.floor(self._simNum/self._simDen)
        rest = self._simNum - integer*self._simDen

        return f"{integer} + {rest}/{self._simDen}"


# ------------------ Operators overloading ------------------

    def __add__(self, other: 'Fraction'):
        """Overloading of the + operator for fractions (return la somme e 2 object fraction)

         PRE : other (class : Fraction) : est un object avec la classe fraction.
         POST : Retourne un object avec la classe fraction qui à en parametres le résultat de la somme des deux
                fractions (self et other).
            exemple :
                - Fraction(10,5); other => Fraction(5,3) => return  Fraction(55, 15)
                - Fraction(10,5); other => Fraction(-5,3) => return  Fraction(5, 15)
         """
        num = self._simNum * other._simDen + other._simNum * self._simDen
        den = self._simDen * other._simDen
        return Fraction(num, den)


    def __sub__(self, other: 'Fraction'):
        """Overloading of the - operator for fractions

        PRE : other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un object avec la classe fraction qui à en parametres le résultat de la soustraction
                des deux fractions (self et other).
            exemple :
                - Fraction(10,5); other = Fraction(5,3) => return  Fraction(5, 15)
                - Fraction(10,5); other = Fraction(-5,3) => return  Fraction(55, 15)
        """
        num = self._simNum * other._simDen - other._simNum * self._simDen
        den = self._simDen * other._simDen
        return Fraction(num, den)


    def __mul__(self, other: 'Fraction'):
        """Overloading of the * operator for fractions

        PRE :  other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un object avec la classe fraction qui à en parametres le résultat de la multiplication
                des deux fractions (self et other).
            exemple :
                - Fraction(10,5); other = Fraction(5,3) => return  Fraction(50,15)
                - Fraction(10,5); other = Fraction(-5,3) => return  Fraction(-50,15)
        """
        num = self._simNum * other._simNum
        den = self._simDen * other._simDen
        return Fraction(num, den)


    def __truediv__(self, other: 'Fraction'):
        """Overloading of the / operator for fractions (avoir un raise si other = 0) (le try exept et pour récupere le raise => ne sert à rien car pour la divison on multiple et divise pas réelement)

        PRE : other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un object avec la classe fraction qui à en parametres le résultat de la multiplication
                des deux fractions (self et other). Le dénominateur ne peut pas etre négatif au retour.
            exemple :
                - Fraction(10,5); other = Fraction(5,3) => return  Fraction(30,25)
                - Fraction(10,5); other = Fraction(-5,3) => return  Fraction(30,-25)
        RAISE : ZeroDivisionError : si le numératuer du other est égal à 0 car on ne peut pas diviser par 0
        """
        if self.numerator == 0:
            raise ZeroDivisionError

        num = self._simNum * other._simDen
        den = self._simDen * other._simNum
        #dénominateur négatif
        if den < 0 :
            num = -num
            den = -den
        return Fraction(num, den)



    def __pow__(self, other: 'Fraction'):
        """Overloading of the ** operator for fractions

        PRE : other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un float qui est égal à la fraction self exposant la fraction other.
            exemple :
                - Fraction(10,5); other = Fraction(5,3) => return  3.175..
                - Fraction(10,5); other = Fraction(-5,3) => return  0.315..
                - Fraction(10,5); other = Fraction(0,3) => return  1
        RAISE : ValueError : on ne peut pas faire 0 exposant un nombre négatif
        """
        base = self._simNum / self._simDen
        exponent = other._simNum / other._simDen
        if base == 0 and exponent < 0:
            raise ValueError

        return round(base**exponent,3)


    def __eq__(self, other: 'Fraction') :
        """Overloading of the == operator for fractions

        PRE : other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un booléen (True/False) disant si valeur de la class Fraction self est égal à la valeur de la class Fraction de other.
            exemple :
                - Fraction(10,5); other = Fraction(5,3) => return  Fasle
                - Fraction(10,5); other = Fraction(2,1) => return  True
        """
        return (self._simNum/self._simDen) == (other._simNum/other._simDen)

    def __float__(self) :
        """Returns the decimal value of the fraction

        PRE : /
        POST : Retourne la valeur décimal de la fraction.
            exemple :
                - Fraction(10,5); => return 2
                - Fraction(-10,5);  => return -2
                - Fraction(12,5);  => return 2.4
        """
        return self._simNum/self._simDen

# TODO : [BONUS] You can overload other operators if you wish (ex : <, >, ...)



# ------------------ Properties checking  ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : /
        POST : Retourne un Booléen (True/False) qui dit si la fraction est égal à 0.
            exemple :
                - Fraction(0,5); => return  True
                - Fraction(10,5);  => return  False
        """
        return self._simNum == 0


    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : /
        POST : Retourne un Booléen (True/False) qui dit si la valeur de la fraction est un integer.
            exemple :
                - Fraction(10,5); => return  True
                - Fraction(7,5);  => return  False
        """
        return self._simNum % self._simDen == 0

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : /
        POST : Retourne un Booléen (True/False) qui dit si la valeur absolue de la fraction est inférieur à 1.
            exemple :
                - Fraction(4,5); => return  True
                - Fraction(10,5);  => return  False
        """
        return abs(self._simNum) < self._simDen

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : /
        POST : Retourne un Booléen (True/False) qui dit si la valeur à la forme simplifier de la fraction est égal à 1.
            exemple :
                - Fraction(1,5); => return  True
                - Fraction(5,5);  => return  True
                - Fraction(10,5);  => return  False
        """

        return self._simNum == 1

    def is_adjacent_to(self, other: 'Fraction') :
        """Check if two fractions differ by a unit fraction

        Two fractions are adjacents if the absolute value of the difference them is a unit fraction

        PRE : other (class : Fraction) : est un object avec la classe fraction.
        POST : Retourne un booléen (True/False) disant si valeur absolue de la class Fraction self est edjacent (+1 ou -1)
                à la valeur absolue de la class Fraction de other.
            exemple :
                - Fraction(10,5); other = Fraction(5,5) => return  True
                - Fraction(0,5); other = Fraction(-5,5) => return  True
                - Fraction(10,5); other = Fraction(-5,5) => return  True
                - Fraction(10,5); other = Fraction(0,5) => return  False
        """
        difference_numerator = self._simNum * other._simDen - other._simNum * self._simDen

        absolute_difference = abs(difference_numerator)
        return absolute_difference == 1



# tests
if __name__ == "__main__" :
    print(f"frac 1 : Fraction(10, -5)\n"
          f"frac 2 : Fraction(-5,-5)")
    test = Fraction(10, -5)
    test2 = Fraction(-5,-5)
    print(f"frac1 num :{test.numerator}")
    print(f"frac1 den : {test.denominator}")
    print(f"frac2 num :{test2.numerator}")
    print(f"frac2 den : {test2.denominator}")
    print(f"__add__ : {test + test2}")
    print(f"__truediv__ : {test.__truediv__(test2)}")
    print(f"__eq__ : {test.__eq__(test2)}")
    print(f"is_zero : {test.is_zero()}")
    print(f"is_adjacent_to : {test.is_adjacent_to(test2)}")

    #test des exeptions
    try :
        frac = Fraction(10, 0)
    except ZeroDivisionError:
        print("ZeroDivisionError : La fraction ne peut pas avoir un dénominateur null")

    try :
        frac1 = Fraction(10, 2)
        frac2 = Fraction(0,2)
        frac1.__truediv__(frac2)
    except ZeroDivisionError :
        print("On ne peut pas diviser par zéro.")

    try :
        frac1 = Fraction(0, 2)
        frac2 = Fraction(-2,2)
        frac1.__pow__(frac2)
    except ValueError :
        print("On ne peut pas diviser 0 par un nombre négatif")