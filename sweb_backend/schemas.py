from sweb_backend.main import MA


class Tree(MA.TableSchema):
	class Meta:
		fields = ("BaumNr", "BaumID", "Pflanzreihe", "PflanzreihePosition", "SortenID", "Sorte", "Frucht", "PatenID", "Longitude", "Latitude")


class Sorten(MA.TableSchema):
	class Meta:
		fields = ("id", "frucht", "sorte", "andereNamen", "herkunft", "groesse", "beschreibung", "reifezeit",
		          "geschmack", "verwendung", "lager", "verbreitung")


class Treecoordinates(MA.TableSchema):
	class Meta:
		fields = ("BaumNr", "Longitude", "Latitude")


class Admin(MA.TableSchema):
	class Meta:
		fields = ("id", "email")


class Image(MA.TableSchema):
	class Meta:
		fields = ("id", "uri")
