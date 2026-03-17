import sqlalchemy
from sqlalchemy.orm import Session
import models, schemas
#1. recuperer un etudiant par son id"""
def get_etudiant(db: Session, etudiant_id: int):
    #""" recupere un etudiant par son id"""
    return db.query(models.EtudiantModel).filter(models.EtudiantModel.id == etudiant_id).first()

#2. recuperer tous les etudiants"""
#def get_etudiants_all(db: Session):
    #return db.query(models.EtudiantModel).offset(skip).limit(limit).all()

#3. recuperer tous les etudiants sans surcharger le serveur(10000 etudiants)
# cette fois ci en limitant le nombre d'etudiants à afficher
def get_etudiants_all_limit(db: Session, skip: int = 0, limit: int = 10):
   #on retourne une liste d'etudiant avec une limie pour ne pas saturer
    return db.query(models.EtudiantModel).offset(skip).limit(limit).all()
#4. cree un nouvel etudiant"""
def create_etudiant(db: Session, etudiant: schemas.EtudiantCreate):
    #on transforme le schema pydantic en modele SQLAlchemy
    db_etudiant = models.EtudiantModel(
        nom=etudiant.nom,
        prenom=etudiant.prenom,
        age=etudiant.age,
        sexe=etudiant.sexe,
        filiere=etudiant.filiere,
        domicile=etudiant.domicile
    )
    
    db.add(db_etudiant) #on prepare l'ajout l'etudiant a la session
    db.commit()#on valide l'écriture dans Mariadb
    db.refresh(db_etudiant) #on ecupere l'etudiant avec son id genere par la base de donnees
    return db_etudiant
    #5. supprimer un etudiant par son id"""
def delete_etudiant(db: Session, etudiant_id: int):
    #1. On cherche d'abord si l'etudiant à supprimer existe dans la base de donnees
    db_etudiant = db.query(models.EtudiantModel).filter(models.EtudiantModel.id == etudiant_id).first()
    if db_etudiant:
        #si l'etudiant existe on le supprime
        db.delete(db_etudiant)
        #3. on valide la suppression dans la base de donnees
        db.commit()
        #on confirme la suppression
        return True
    return False #on signale que l'etudiant n'existe pas et donc ne peut pas etre supprime