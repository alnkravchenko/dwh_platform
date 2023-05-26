from typing import List, Tuple
from uuid import UUID

from repos import projects as proj_db
from schema.project import ProjectContent, ProjectCreate, ProjectModel, ProjectUpdate
from schema.user import UserModel
from sqlalchemy.orm import Session


class ProjectService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def validate_user_access(self, project_id: UUID) -> Tuple[int, str]:
        # check if project exists
        proj = proj_db.get_project_by_id(self.db, project_id)
        if proj is None:
            return 404, "Not found"
        # check user access
        if proj.created_by != self.user.id:
            return 401, "Unauthorized"
        return 200, "OK"

    def get_user_projects(self) -> List[ProjectModel]:
        projects = proj_db.get_user_projects(self.db, self.user.id, limit=None)
        return projects

    def get_project_content(self, project_id: UUID) -> Tuple[int, str | ProjectContent]:
        content = proj_db.get_content(self.db, self.user.id, project_id)
        if content is None:
            return 404, "Not found"
        return 200, content

    def create_project(self, project: ProjectCreate) -> Tuple[int, str]:
        proj_db.create_project(self.db, project, self.user.id)
        return 200, "Project created"

    def update_project(
        self, project_id: UUID, new_data: ProjectUpdate
    ) -> Tuple[int, str]:
        new_proj = proj_db.update_project(self.db, project_id, new_data)
        if new_proj is None:
            return 400, "Bad request"
        return 200, f"Project(id={project_id}) updated"

    def delete_project(self, project_id: UUID) -> Tuple[int, str]:
        is_deleted = proj_db.delete_project_by_id(self.db, project_id)
        if not is_deleted:
            return 400, "Bad request"
        return 200, f"Project(id={project_id}) deleted"
