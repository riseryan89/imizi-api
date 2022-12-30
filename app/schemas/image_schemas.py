from pydantic import BaseModel, Field


class UploadImageREQ(BaseModel):
    image_base64: str = Field(..., description="Image Base64 String")
    image_file_name: str = Field(..., description="Human Readable Image Name")


class NewImageGroupREQ(BaseModel):
    image_group_name: str = Field(..., description="Image Group Name")


class ImageGroupRES(BaseModel):
    id: int
    image_group_name: str
    image_count: int

    class Config:
        orm_mode = True


class ImageInfoRES(BaseModel):
    id: int
    image_group: ImageGroupRES
    uuid: str
    file_name: str
    file_extension: str
    total_file_size: int
    image_url_data: dict

    class Config:
        orm_mode = True
