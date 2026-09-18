from pydantic import BaseModel,Field,field_validator

class Detection(BaseModel):
    frame:int=Field(ge=0)
    track_id:int|None=Field(default=None,ge=0)
    label:str=Field(min_length=1,max_length=100)
    confidence:float=Field(ge=0.0,le=1.0)
    bbox:tuple[float,float,float,float]
    @field_validator("bbox")
    @classmethod
    def valid_bbox(cls,value):
        x1,y1,x2,y2=value
        if x2<x1 or y2<y1: raise ValueError("Invalid bounding box")
        return value

class ReviewDecision(BaseModel):
    decision:str
    reviewer:str=Field(default="human",min_length=1,max_length=100)
    final_label:str|None=Field(default=None,max_length=100)

class TrackSummary(BaseModel):
    track_id:int
    label:str
    first_frame:int
    last_frame:int
    frames_seen:int
    mean_confidence:float
