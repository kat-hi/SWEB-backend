from main import MA


class Tree(MA.TableSchema):
	class Meta:
		fields = ("id", "sortenID", "sorte", "frucht", "sorte", "longitude", "latitude", "pate")


class Sorten(MA.TableSchema):
	class Meta:
		fields = ("id", "frucht", "sorte", "andereNamen", "herkunft", "groesse", "beschreibung", "reifezeit",
		          "geschmack", "verwendung", "lager", "verbreitung")


class Treecoordinates(MA.TableSchema):
	class Meta:
		fields = ("id", "longitude", "latitude")


class Admin(MA.TableSchema):
	class Meta:
		fields = ("id", "username", "password")
