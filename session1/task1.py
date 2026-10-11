from pydantic import BaseModel,Field,field_validator
from groq import Groq
class userProfile(BaseModel):
    name: str= Field(description="full name"),
    age: int= Field(gt=18,description="Age"),
    @field_validator("name")
    def no_space(cls,v:str)-> str:
        if " " in v:
            raise ValueError("username has spaces")
        return v
client= Groq()
completion= client.chat.completions.create(
    model= "openai/gpt-oss-120b",
    messages=[
              {"role": "user","content":"suggest me unique and age  and output should be in json format"
    }],
    response_format={"type": "json_object"},

)
print(completion.choices[0].message.content)