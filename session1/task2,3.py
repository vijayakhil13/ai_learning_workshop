import instructor
from groq import Groq
from pydantic import BaseModel
class d(BaseModel):
    name: str
    age: int
client=instructor.from_groq(Groq())
user: d=client.chat.completions.create(
    model= "openai/gpt-oss-120b",
    response_model=d,
    messages=[{"role":"user","content":"extract: vineeth is 25 years old"}]
)
print(user.age)
print(user.name)
import tiktoken
encoding=tiktoken.get_encoding("cl100k_base")
text= "myself vineeth"
token=encoding.encode(text)
print(token)
print(len(token))