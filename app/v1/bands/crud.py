from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .models import Band
from .schemas import BandSchema


def get_band(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of Band records with pagination.
    """
    bands = db.query(Band).offset(skip).limit(limit).all()
    return jsonable_encoder(bands)

def get_band_by_id(db: Session, band_id: int):
    """
    Retrieve a single Band record by ID.
    """
    return db.query(Band).filter(Band.id == band_id).first()

def create_band(db: Session, band: BandSchema):
    """
    Create a new Band record in the database.
    """
    _band = Band(
        name=band.name,
        description=band.description,
        image=band.image,
    )
    db.add(_band)
    db.commit()
    db.refresh(_band)
    return jsonable_encoder(_band)

def update_band(db: Session, band_id: int, name: str = None, description: str = None, image: str = None):
    """
    Update an existing Band record in the database.
    """
    _band = db.query(Band).filter(Band.id == band_id).first()
    if not _band:
        raise ValueError(f"Band with id {band_id} does not exist")

    if name is not None:
        _band.name = name
    if description is not None:
        _band.description = description
    if image is not None:
        _band.image = image

    db.commit()
    db.refresh(_band)
    return jsonable_encoder(_band)

def remove_band(db: Session, band_id: int):
    """
    Delete a Band record by ID.
    """
    _band = get_band_by_id(db=db, band_id=band_id)
    if not _band:
        raise ValueError(f"Band with id {band_id} does not exist")

    db.delete(_band)
    db.commit()
    return jsonable_encoder(_band)