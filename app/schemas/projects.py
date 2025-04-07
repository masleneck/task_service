from pydantic import BaseModel, ConfigDict

class ProjectCreateRequest(BaseModel):
    slug: str  

    model_config = ConfigDict(from_attributes=True)