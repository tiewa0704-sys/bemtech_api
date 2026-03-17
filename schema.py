from pydantic import BaseModel
from typing import Optional
#1. Le schéma de base :ce qui est commun à la création  
class EtudiantBase(BaseModel):
    nom: str
    prenom: str
    age: int
    filiere: str
    domicile: str
#2. pour la création d'un étudiant (post)
class EtudiantCreate(EtudiantBase):
    pass
#3. pour modifier un étudiant (tous les champs sont optionnels)
class EtudiantUpdate(EtudiantBase):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    age: Optional[int] = None
    filiere: Optional[str] = None
    domicile: Optional[str] = None
#4. schéma pour la réponse
class Etudiant(EtudiantBase):
    id: int #la reponse contient toujours l'ID généré
    class Config:
        orm_mode = True #permet à pydantic de lire les objets SQLAlchemy