from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
from pydantic import ValidationError
import json


# ______________________________________Модель для коллекции______________________________________
class Metadata(BaseModel):
    cover_image: Optional[HttpUrl]
    description: str
    marketplace: str
    external_url: Optional[HttpUrl]
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
    collection: Optional[Union[str, NFTCollection]] = None
    metadata: NFTMetadata
    previews: List[NFTItemPreview]


class NFTItemsModel(BaseModel):
    nft_items: List[NFTItem]


# ______________________________________Модель для nft_______________________________________________
from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl


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


class SalePrice(BaseModel):
    value: str
    token_name: str


class SaleInfo(BaseModel):
    contract_address: str
    owner_address: str
    price: SalePrice


class ONE_NFT_Item_Model(BaseModel):
    address: str
    index: int
    owner_address: str
    collection: Optional[Union[str, Collection]] = None
    metadata: ONE_NFT_Metadata
    sale: Optional[SaleInfo] = None
    previews: List[NFT_Preview]

# ______________________________Модель для топа_____________________
class NFTCollectionMetadataSchema(BaseModel):
    cover_image: Optional[HttpUrl] = None
    description: str = ""
    marketplace: str = ""
    external_url: Optional[HttpUrl] = None
    social_links: List[HttpUrl] = []
    name: str = ""
    image: Optional[HttpUrl] = None


class NFTCollectionSchema(BaseModel):
    address: str
    raw_address: str
    metadata: NFTCollectionMetadataSchema
    hype: int
    owner_address: str
    items_count: int
    previews: List[Preview]


class TopNFTCollectionSchema(BaseModel):
    collections: List[NFTCollectionSchema] = []
    total_count: int
    page: int
    page_size: int


class Price(BaseModel):
    value: str
    token_name: str


class Sale(BaseModel):
    contract_address: str
    owner_address: str
    price: Price


class NFTItemMetadata(BaseModel):
    description: str = ""
    marketplace: str = ""
    name: str = ""
    image: Optional[HttpUrl] = None


class NFTItemSchema(BaseModel):
    address: str
    raw_address: str
    index: int
    owner_address: Optional[str] = None
    collection: Optional[Collection] = None
    metadata: NFTItemMetadata
    hype: int
    sale: Optional[Sale] = None
    previews: List[Preview]


class NFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema] = []


class TopNFTItemsSchema(BaseModel):
    nft_items: List[NFTItemSchema]
    total_count: int
    page: int
    page_size: int


# _____________________________Модель для итемов профиля__________________________
class NFTItemsSchema_Profile_Items(BaseModel):
    nft_items: List[NFTItemSchema] = []