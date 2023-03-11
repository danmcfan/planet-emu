import json
from typing import Any, Hashable

import geopandas as gpd
from sqlalchemy.orm import Session

from planet_emu.api import models


def create_result(
    db: Session, id: str, x: float, y: float, year: int, properties: dict[Hashable, Any]
) -> models.Result:
    result = models.Result(id=id, x=x, y=y, year=year, properties=properties)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_results(db: Session, skip: int = 0, limit: int = 100) -> list[models.Result]:
    return db.query(models.Result).offset(skip).limit(limit).all()


def get_result(db: Session, id: str) -> models.Result:
    return db.query(models.Result).filter(models.Result.id == id).first()


def get_state_names(db: Session) -> list[str]:
    return (
        db.execute("SELECT DISTINCT state_name FROM counties ORDER BY 1 ASC")
        .scalars()
        .all()
    )


def get_county_names(db: Session, state_name: str) -> list[str]:
    return (
        db.execute(
            "SELECT DISTINCT county_name FROM counties WHERE state_name = '{}' ORDER BY 1 ASC".format(
                state_name.title()
            )
        )
        .scalars()
        .all()
    )


def get_counties_by_state_name(db: Session, state_name: str) -> dict[Hashable, Any]:
    gdf = gpd.read_postgis(
        "SELECT * FROM counties WHERE state_name = '{}'".format(state_name.title()),
        db.get_bind(),
        geom_col="geometry",
        index_col="index",
        crs="EPSG:4326",
    )
    return json.loads(gdf.to_json())
