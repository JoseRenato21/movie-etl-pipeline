from dotenv import load_dotenv
import os
import httpx

def extract() -> list[dict]:
    
    load_dotenv()
    token = os.getenv("TMDB_API_TOKEN")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = []
    try:   
        for n in range(1, 10):
            response = httpx.get(f"https://api.themoviedb.org/3/movie/popular?page={n}", headers=headers)
            response.raise_for_status() 
            data.append(response.json())
        return data
    except httpx.HTTPStatusError as e:
        print(e)
    except httpx.RequestError as e:
        print(e)
        
