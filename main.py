from fastapi import FastAPI,Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session

# On importe nos propres fichiers
import models,schemas,operations
from database import get_db,engine

# On initialise l'application
app=FastAPI(title="BEMTECH API- Gestion des Etudiants")

# Creer une route standard avec la version pour toutes les methodes
# Desormais toutes nos routes serot attachées au ROUTEUR (au lieu de app)
router_v2 = APIRouter(prefix="/bemtech/v2",tags=["Version 2"])

# Route pour afficher tous les etudiants
#@router_v2.get("/etudiants/", response_model=list[schemas.EtudiantResponse])
#def lire_tous_les_etudiants(db: Session = Depends(get_db)):
#    return operations.get_etudiants_all(db)

# Une autre route pour afficher tous les etudiants
#  mais cette fois-ci en limitant le nombre d'etudiants à afficher
@router_v2.get("/etudiants/", response_model=list[schemas.EtudiantResponse])
def lire_les_etudiants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Récupère tous les étudiants avec option de pagination"""
    db_etudiants = operations.get_etudiants_all_limit(db, skip=skip, limit=limit)
    return db_etudiants

# Route pour afficher un etudiant par son id
@router_v2.get("/etudiants/{id_recherche}",response_model=schemas.EtudiantResponse)
def lire_etudiant_id(id_recherche:int,db:Session = Depends(get_db)):
    db_etudiant = operations.get_etudiant_by_id(db,etudiant_id=id_recherche)
     # Si la base de données ne trouve rien (None)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail="Etudiant non trouvé dans MariaDB")
    return db_etudiant


# Route pour CRÉER un étudiant (POST)
# Note : on utilise status_code 201 comme on l'a vu ensemble !
@router_v2.post("/etudiants/", response_model=schemas.EtudiantResponse, status_code=status.HTTP_201_CREATED)
def creer_etudiant(etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    return operations.create_etudiant(db=db, etudiant=etudiant)

# Route pour supprimer un etudiant
@router_v2.delete("/etudiants/{id_recherche}",status_code= status.HTTP_204_NO_CONTENT)
def supprimer_etudiant(id_recherche,db:Session=Depends(get_db)):
    reussite = operations.delete_etudiant(db,etudiant_id=id_recherche)
    if not reussite:
        raise HTTPException(
            status_code=404, 
            detail=f"Impossible de supprimer : l'étudiant avec l'ID {id_recherche} n'existe pas."
        )
    
    # Avec le code 204, FastAPI ne renverra aucun corps de message (c'est le standard)
    return None
# ENFIN, on inclut le routeur dans l'application principale
app.include_router(router_v2)
