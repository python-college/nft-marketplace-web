from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
from pydantic import ValidationError
import json


# ______________________________________Модель для коллекции______________________________________
class Metadata(BaseModel):
    cover_image: Optional[HttpUrl]  # Теперь можно передавать None
    description: str
    marketplace: str
    external_url: Optional[HttpUrl]  # Теперь можно передавать None
    social_links: List[str]
    name: str
    image: HttpUrl


class Preview(BaseModel):
    resolution: str
    url: HttpUrl


class NFTModel(BaseModel):
    metadata: Metadata
    address: str
    owner_address: str
    items_count: int
    previews: List[Preview]

# ______________________________________Модель для итемов коллекции______________________________________
class NFTMetadata(BaseModel):
    description: str
    marketplace: str
    name: str
    image: HttpUrl


class NFTItemPreview(BaseModel):
    resolution: str
    url: HttpUrl


class NFTCollection(BaseModel):
    address: str
    name: str
    description: str

class NFTItem(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: Optional[Union[str, NFTCollection]] = None  # Допускаем объект или строку
    metadata: NFTMetadata
    previews: List[NFTItemPreview]


class NFTItemsModel(BaseModel):
    nft_items: List[NFTItem]


# ______________________________________Модель для nft_______________________________________________
class ONE_NFT_Metadata(BaseModel):
    description: str
    marketplace: str
    name: str
    image: HttpUrl

class NFT_Preview(BaseModel):
    resolution: str
    url: HttpUrl

class Collection(BaseModel):
    address: str
    name: str
    description: str

class ONE_NFT_Item_Model(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: Optional[Union[str, Collection]] = None
    metadata: ONE_NFT_Metadata
    previews: List[NFT_Preview]
