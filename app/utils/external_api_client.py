import httpx

async def fetch_product_details(product_id: int):
    url = f"https://external.sampleapi.com/products/{product_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

