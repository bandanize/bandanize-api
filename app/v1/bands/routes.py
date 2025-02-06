from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import BandSchema, RequestBand, RequestDelete, RequestUpdate, Response
from ..config import SessionLocal
from . import crud

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=Response[BandSchema])
async def create_band_service(request: RequestBand, db: Session = Depends(get_db)):
    """
    Creates a new Band entry in the database.
    """
    try:
        band = crud.create_band(db, band=request.parameter)
        return Response(
            status="Ok",
            code="200",
            message="Band created successfully",
            result=BandSchema.model_validate(band)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=Response[list[BandSchema]])
async def get_bands(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of Band entries from the database.
    """
    try:
        bands = crud.get_band(db, skip, limit)
        return Response(
            status="Ok",
            code="200",
            message="Successfully fetched all data",
            result=[BandSchema.model_validate(band) for band in bands]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{band_id}", response_model=Response[BandSchema])
async def get_band_by_id(band_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single Band entry by ID from the database.
    """
    try:
        band = crud.get_band_by_id(db, band_id=band_id)
        if band is None:
            raise HTTPException(status_code=404, detail=f"Band with id {band_id} does not exist")
        return Response(
            status="Ok",
            code="200",
            message="Successfully fetched data",
            result=BandSchema.model_validate(band)
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/update", response_model=Response[BandSchema])
async def update_band(request: RequestUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing Band entry based on ID.
    """
    try:
        band = crud.update_band(
            db, 
            band_id=request.parameter.id,
            name=request.parameter.name, 
            description=request.parameter.description,
            image=request.parameter.image,
        )
        return Response(
            status="Ok",
            code="200",
            message="Successfully updated data",
            result=BandSchema.model_validate(band)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete", response_model=Response[None])
async def delete_band(request: RequestDelete, db: Session = Depends(get_db)):
    """
    Deletes a Band entry based on ID.
    """
    try:
        band_id = request.parameter.id
        band_instance = crud.get_band_by_id(db, band_id=band_id)
        if band_instance is None:
            raise HTTPException(status_code=404, detail=f"Band with id {band_id} does not exist")
        
        crud.remove_band(db, band_id=band_id)
        return Response(
            status="Ok",
            code="200",
            message="Successfully deleted data",
            result=None
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))