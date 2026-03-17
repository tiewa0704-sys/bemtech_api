from sqlalchemy import Column, Integer, String
from database import Base

#On definit notre classe qui va correspondre à notre table dans la base de données

class EtudiantModel(Base):
    #le nom exact dans mysql
    __tablename__ = "etudiants"

    #On va definir les colonnes de notre table

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(20), nullable=False)
    prenom = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    sexe = Column(String(1), nullable=False)
    filiere = Column(String(10), nullable=False)
    domicile = Column(String(30), nullable=False)