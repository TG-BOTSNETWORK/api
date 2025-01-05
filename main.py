from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import instaloader


app = FastAPI(title="Instagram Profile API", version="1.0.0")

class ProfileResponse(BaseModel):
    username: str
    full_name: str
    bio: str
    profile_pic_url: str
    profile_url: str

@app.get("/profile/{username}", response_model=ProfileResponse)
async def get_instagram_profile(username: str):
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return ProfileResponse(
            username=profile.username,
            full_name=profile.full_name,
            bio=profile.biography,
            profile_pic_url=profile.profile_pic_url,
            profile_url=f"https://www.instagram.com/{profile.username}/"
        )
    except instaloader.exceptions.ProfileNotExistsException:
        raise HTTPException(status_code=404, detail="Profile not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
