from pydantic import BaseModel, Field


class UploadImageREQ(BaseModel):
    image: str = Field(..., description="Image Base64 String")
    image_name: str = Field(..., description="Human Readable Image Name")


class NewImageGroupREQ(BaseModel):
    image_group_name: str = Field(..., description="Image Group Name")


class ImageGroupRES(BaseModel):
    image_group_name: str
    image_count: int
