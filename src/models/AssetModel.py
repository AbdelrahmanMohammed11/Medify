from .BaseDataModel import BaseDataModel
from .DB_Schema.Med_Rag.schemes import Asset
from .enums.DBEnums import DBEnums
from sqlalchemy.future import select
from sqlalchemy import func


class AssetModel(BaseDataModel):
    
    def __init__(self, db_clint: object):
        super().__init__(db_clint= db_clint)
        self.db_clint = db_clint


    @classmethod
    async def create_instance(cls, db_clint: object):
       
        """
        Create an instance of the assetModel class.
        """
        instance = cls(db_clint)
        return instance


    async def create_asset(self, asset: Asset):
        """
        Create a new asset in the database.
        """
        async with self.db_clint() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)

        return asset
    
    async def get_all_assets_of_project(self, asset_project_id:int, asset_type: str):

            async with self.db_clint() as session:

                 query = await session.execute(
                      select(Asset).where(
                            Asset.asset_project_id == asset_project_id,
                            Asset.asset_type == asset_type
                      )
                      )
                 records = query.scalars().all()
            return records 
    
    async def get_asset(self, asset_project_id:int, asset_name: str):

            async with self.db_clint() as session:

                 query = await session.execute(
                      select(Asset).where(
                            Asset.asset_project_id == asset_project_id,
                            Asset.asset_name == asset_name
                      )
                      )
                 records = query.scalar_one_or_none()
            return records
