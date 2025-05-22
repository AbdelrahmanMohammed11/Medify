from .BaseDataModel import BaseDataModel
from .DB_Schema.Med_Rag.schemes import Project
from .enums.DBEnums import DBEnums
from sqlalchemy.future import select
from sqlalchemy import func


class ProjectModel(BaseDataModel):
    
    def __init__(self, db_clint: object):
        super().__init__(db_clint= db_clint)
        self.db_clint = db_clint


    @classmethod
    async def create_instance(cls, db_clint: object):
       
        """
        Create an instance of the ProjectModel class.
        """
        instance = cls(db_clint)
        return instance


    async def create_project(self, project: Project):
        """
        Create a new project in the database.
        """
        async with self.db_clint() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)

        return project
    
    async def get_project_or_create_new_one(self, project_id: str):
            """
            Get a project by name or create a new one if it doesn't exist.
            Args:
                project_name (str): The name of the project to retrieve or create.
            Returns:
                Project: The retrieved or newly created project.
            """
            async with self.db_clint() as session:
                async with session.begin():
                     
                    # Check if the project already exists
                     query = select(Project).where(Project.project_id == project_id)
                     result = await session.execute(query)
                     project = result.scalar_one_or_none()
                     if project is None:
                         
                        # Create a new project if it doesn't exist
                         project_record = Project(
                             project_id=project_id
                            )
                         project = await self.create_project(project= project_record)
                         return project
                     else:
                         return project
                     
    async def get_all_project(self, page: int = 1, page_size: int = 10):
            """
            Get all projects from the database with pagination.
            Args:
                page (int): The page number to retrieve.
                page_size (int): The number of projects per page.
            Returns:
                list: A list of projects for the specified page.
            """
            async with self.db_clint() as session:
                async with session.begin():
                     # Count the total number of projects
                     # This is done to calculate the total number of pages
                     total_projects = await session.execute(select(
                          func.count(Project.project_id)
                                                                   ))
                     total_projects = total_projects.scalar_one()

                     """
                     Calculate the total number of pages and if the total number projects % page_size > 0
                        then add 1 to the total number of pages
                     """
                     total_pages = (total_projects // page_size) + (1 if total_projects % page_size > 0 else 0)
                    
                    
                    # Equivalent to :
                    #if total_projects // total_pages > 0:
                    #    total_pages += 1

                     """
                     offset is used to skip the number of projects in the previous pages
                     """
                     query = select(Project).offset((page - 1) * page_size).limit(page_size)
                     projects = await session.execute(query).scalars().all()

                     return projects, total_pages

                     